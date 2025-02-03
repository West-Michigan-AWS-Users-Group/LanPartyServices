from aws_cdk import (
    CfnOutput,
    Stack,
    Tags,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)
from constructs import Construct

used_azs = {"us-east-2": ["us-east-2a"]}


class Core(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # add tags
        Tags.of(self).add("service", self.__class__.__name__)
        stack_name_ansi = (
            self.__class__.__name__.replace("-", "")
            .replace("_", "")
            .replace(".", "")
            .capitalize()
        )
        stack_name_parts = self.stack_name.split("-")
        environment = stack_name_parts[0]

        vpc = ec2.Vpc(
            self,
            f"{environment}{stack_name_ansi}VPC",
            max_azs=len(used_azs),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=20,
                ),
            ],
        )

        for subnet in vpc.public_subnets:
            Tags.of(subnet).add("aws-cdk:subnet-type", "Public")

        for subnet in vpc.private_subnets:
            Tags.of(subnet).add("aws-cdk:subnet-type", "Private")

        cluster = ecs.Cluster(self, f"{stack_name_ansi}LanPartyServers", vpc=vpc)

        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}VpcId",
            value=vpc.vpc_id,
            export_name=f"{environment}{stack_name_ansi}VpcId",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}LanPartyServersClusterName",
            value=cluster.cluster_name,
            export_name=f"{environment}{stack_name_ansi}LanPartyServersClusterName",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicSubnetIds",
            value=",".join([subnet.subnet_id for subnet in vpc.public_subnets]),
            export_name=f"{environment}{stack_name_ansi}PublicSubnetIds",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PrivateSubnetIds",
            value=",".join([subnet.subnet_id for subnet in vpc.private_subnets]),
            export_name=f"{environment}{stack_name_ansi}PrivateSubnetIds",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicRouteTableIds",
            value=",".join(
                [subnet.route_table.route_table_id for subnet in vpc.public_subnets]
            ),
            export_name=f"{environment}{stack_name_ansi}PublicRouteTableIds",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PrivateRouteTableIds",
            value=",".join(
                [subnet.route_table.route_table_id for subnet in vpc.private_subnets]
            ),
            export_name=f"{environment}{stack_name_ansi}PrivateRouteTableIds",
        )
