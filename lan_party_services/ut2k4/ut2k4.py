import os

from aws_cdk import (
    Duration,
    Fn,
    Stack,
    Tags,
    aws_ec2 as ec2,
    aws_ecr_assets as ecr_assets,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_logs as logs,
    aws_route53 as route53,
    aws_route53_targets as targets,
)
from constructs import Construct

from lan_party_services.common.cloudwatch import create_cloudwatch_resources
from lan_party_services.core.core import used_azs


class ut2k4(Stack):
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
        # NLB
        nlb_tg_sg_id = Fn.import_value(f"{nlb_import_prefix}NlbTgSGId")
        nlb_tg_security_group = ec2.SecurityGroup.from_security_group_id(
            self, f"{environment}ImportedNlbTgSG", nlb_tg_sg_id
        )
        nlb_arn = Fn.import_value(f"{nlb_import_prefix}PublicNLBArn")
        nlb_dns_name = Fn.import_value(f"{nlb_import_prefix}PublicNLBDnsName")
        nlb_canonical_hosted_zone_id = Fn.import_value(
            f"{nlb_import_prefix}PublicNLBCanonicalHostedZoneId"
        )
        nlb = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(
            self,
            f"{stack_name_ansi}ImportedNLB",
            load_balancer_arn=nlb_arn,
            vpc=vpc,
            load_balancer_canonical_hosted_zone_id=nlb_canonical_hosted_zone_id,
            load_balancer_dns_name=nlb_dns_name,
        )

        ### Server config -
        # Game modes https://wiki.unrealadmin.org/Gametype_List_%28UT2004%29
        # Mutators https://wiki.unrealadmin.org/Mutator_List_%28UT2004%29
        ffa_dm_deck17_vanilla = "DM-Deck17?game=XGame.xDeathMatch?mutator=XGame.MutInstaGib,UnrealGame.MutLowGrav"
        ffa_dm_osiris2_instagib = "DM-DE-Osiris2?game=XGame.xDeathMatch?mutator=XGame.MutInstaGib"
        team_dm_vanilla = "DM-DE-Grendelkeep?game=XGame.xTeamGame"
        ctf_facing_worlds_low_grav = "CTF-FaceClassic?game=XGame.xCTFGame?mutator=UnrealGame.MutLowGrav"
        onslaught_robot_factory_vanilla = "AS-RobotFactory?game=XGame.xOnSlaught"

        # Server start command
        server_start_command = team_dm_vanilla

        # Define log strings to send to Discord, messages matching any of this string will be sent to Discord
        log_strings = ["___New Player Joined -", "UTServerAdmin Initialized", "SIGTERM"]

        # Networking
        app_ports = [
            {"port": 7777, "protocol": ecs.Protocol.UDP},
            {"port": 7778, "protocol": ecs.Protocol.UDP},
            {"port": 7787, "protocol": ecs.Protocol.UDP},
            {"port": 28902, "protocol": ecs.Protocol.TCP},
        ]
        health_check_port = 8080
        server_url = f"{app_group_l}.grlanparty.info"
        # Image
        image = ecr_assets.DockerImageAsset(
            self,
            f"{stack_name_ansi}Image",
            directory=os.path.join(os.path.dirname(__file__), "..", app_group_l),
            platform=ecr_assets.Platform.LINUX_AMD64,
        )
        # Logging
        log_group = logs.LogGroup(
            self, f"{stack_name_ansi}LogGroup", retention=logs.RetentionDays.ONE_DAY
        )

        # Permissions
        task_role = iam.Role(
            self,
            f"{stack_name_ansi}TaskRole",
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

        # Create a Fargate task definition with shared memory and CPU resources
        task_definition = ecs.FargateTaskDefinition(
            self,
            f"{stack_name_ansi}TaskDef",
            task_role=task_role,
            memory_limit_mib=1024,
            cpu=512,
        )

        # Sidecar container for health checks - uses busybox to respond to http requests
        health_check_container = task_definition.add_container(
            f"{stack_name_ansi}Healthcheck",
            image=ecs.ContainerImage.from_registry("busybox:latest"),
            essential=True,
            command=[
                "sh",
                "-c",
                "while true; do { echo -e 'HTTP/1.1 200 OK\r\n'; echo 'ok'; } | nc -l -p 8080; done",
            ],
        )
        health_check_container.add_port_mappings(
            ecs.PortMapping(container_port=health_check_port, protocol=ecs.Protocol.TCP)
        )

        # Main container
        main_container = task_definition.add_container(
            f"{stack_name_ansi}Container",
            image=ecs.ContainerImage.from_docker_image_asset(image),
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f"{stack_name_ansi}", log_group=log_group
            ),
            command=[
                "ucc-bin",
                "server",
                server_start_command,
                "-nohomedir",
                "-lanplay",
            ],
        )

        # Create the Fargate service
        service = ecs.FargateService(
            self,
            f"{stack_name_ansi}Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            security_groups=[nlb_tg_security_group],
        )
        # Add port mappings
        for app_port in app_ports:
            main_container.add_port_mappings(
                ecs.PortMapping(
                    container_port=app_port["port"], protocol=app_port["protocol"]
                )
            )

            # Add SG rules to NLB in core stack
            if app_port["protocol"] == ecs.Protocol.UDP:
                nlb_tg_security_group.add_ingress_rule(
                    ec2.Peer.any_ipv4(),
                    ec2.Port.udp(app_port["port"]),
                    f"Allow UDP traffic on {app_port['port']}",
                )
            else:
                nlb_tg_security_group.add_ingress_rule(
                    ec2.Peer.any_ipv4(),
                    ec2.Port.tcp(app_port["port"]),
                    f"Allow TCP traffic on {app_port['port']}",
                )

            # Add listener
            listener_protocol = (
                elbv2.Protocol.UDP
                if app_port["protocol"] == ecs.Protocol.UDP
                else elbv2.Protocol.TCP
            )
            listener = nlb.add_listener(
                f"{stack_name_ansi}Listener{app_port['port']}",
                port=app_port["port"],
                protocol=listener_protocol,
            )
            listener.add_targets(
                f"{stack_name_ansi}FargateServiceTarget{app_port['port']}",
                port=app_port["port"],
                protocol=listener_protocol,
                targets=[
                    service.load_balancer_target(
                        container_name=f"{stack_name_ansi}Container",
                        container_port=app_port["port"],
                        protocol=app_port["protocol"],
                    )
                ],
                health_check=elbv2.HealthCheck(
                    interval=Duration.seconds(15),
                    timeout=Duration.seconds(10),
                    healthy_threshold_count=2,
                    unhealthy_threshold_count=2,
                    port=str(health_check_port),
                    protocol=elbv2.Protocol.TCP,
                ),
                deregistration_delay=Duration.seconds(0),
            )

        # Add health check port to the security group
        nlb_tg_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(health_check_port),
            f"Allow TCP traffic on {health_check_port}",
        )

        # Add a DNS record to the zone named grlanparty.info
        zone = route53.HostedZone.from_lookup(
            self, f"{stack_name_ansi}Zone", domain_name="grlanparty.info"
        )
        route53.ARecord(
            self,
            f"{stack_name_ansi}AliasRecord",
            record_name=server_url,
            target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(nlb)),
            zone=zone,
        )

        create_cloudwatch_resources(
            self, self.stack_name, cluster, service, nlb, log_group, log_strings
        )
