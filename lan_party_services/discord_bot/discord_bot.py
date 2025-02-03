import os

from aws_cdk import (
    Fn,
    Stack,
    Tags,
    aws_ec2 as ec2,
    aws_ecr_assets as ecr_assets,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_logs as logs,
    aws_ssm as ssm,
)
from constructs import Construct

from lan_party_services.core.core import used_azs


class DiscordBot(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        stack_name_ansi = (
            self.__class__.__name__.replace("-", "")
            .replace("_", "")
            .replace(".", "")
            .capitalize()
        )
        stack_name_parts = self.stack_name.split("-")
        environment = stack_name_parts[0]
        app_group = stack_name_ansi
        app_group_l = app_group.lower()
        # add tags
        Tags.of(self).add("service", app_group)

        ### Core stack imports
        core_import_prefix = f"{environment}Core"
        nlb_import_prefix = f"{environment}Nlb"
        vpc_id = Fn.import_value(f"{core_import_prefix}VpcId")
        private_subnet_ids = Fn.import_value(
            f"{core_import_prefix}PrivateSubnetIds"
        ).split(",")
        public_subnet_ids = Fn.import_value(
            f"{core_import_prefix}PublicSubnetIds"
        ).split(",")
        private_route_table_ids = Fn.import_value(
            f"{core_import_prefix}PrivateRouteTableIds"
        ).split(",")
        public_route_table_ids = Fn.import_value(
            f"{core_import_prefix}PublicRouteTableIds"
        ).split(",")
        vpc = ec2.Vpc.from_vpc_attributes(
            self,
            f"{stack_name_ansi}CoreVPC",
            vpc_id=vpc_id,
            availability_zones=used_azs["us-east-2"],
            private_subnet_ids=private_subnet_ids,
            public_subnet_ids=public_subnet_ids,
            private_subnet_route_table_ids=private_route_table_ids,
            public_subnet_route_table_ids=public_route_table_ids,
        )
        # Cluster
        cluster_name = Fn.import_value(
            f"{core_import_prefix}LanPartyServersClusterName"
        )
        cluster = ecs.Cluster.from_cluster_attributes(
            self, cluster_name, cluster_name=cluster_name, vpc=vpc
        )

        ### Server config -

        # Image
        image = ecr_assets.DockerImageAsset(
            self,
            f"{app_group}Image",
            directory=os.path.join(os.path.dirname(__file__), "app"),
        )
        # Logging
        log_group = logs.LogGroup(
            self, f"{app_group}LogGroup", retention=logs.RetentionDays.ONE_DAY
        )

        # Permissions
        task_role = iam.Role(
            self,
            f"{app_group}TaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            inline_policies={
                "CloudWatchLogsPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                            resources=[log_group.log_group_arn],
                        )
                    ]
                )
            },
        )

        # Create a Fargate service
        task_definition = ecs.FargateTaskDefinition(
            self,
            f"{app_group}TaskDef",
            task_role=task_role,
            cpu=256,
            memory_limit_mib=512,
        )

        # Fetch the secure SSM parameter
        discord_bot_client_token = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "DiscordBotClientToken",
            parameter_name="/prod/lan_party_services/discord_bot/discord_bot_client_token",
            version=1,
        )

        # Main container with health check and secrets
        main_container = task_definition.add_container(
            f"{app_group_l}-container",
            image=ecs.ContainerImage.from_docker_image_asset(image),
            memory_limit_mib=256,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=app_group, log_group=log_group
            ),
            secrets={
                "DISCORD_BOT_CLIENT_TOKEN": ecs.Secret.from_ssm_parameter(
                    discord_bot_client_token
                ),
            },
            # health_check=ecs.HealthCheck(
            #     command=["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
            #     interval=Duration.seconds(30),
            #     timeout=Duration.seconds(5),
            #     retries=3,
            #     start_period=Duration.seconds(60),
            # ),
        )

        # Create the Fargate service
        service = ecs.FargateService(
            self,
            f"{app_group}Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
        )
