from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    CfnOutput,
    Tags
)
from constructs import Construct

used_azs = {
    'us-east-2': ['us-east-2a']
}

class CoreStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # add tags
        Tags.of(self).add("service", "LanPartyServices")
        Tags.of(self).add("stack", self.__class__.__name__)

        vpc = ec2.Vpc(self, "CoreVPC", max_azs=len(used_azs), subnet_configuration=[
            ec2.SubnetConfiguration(
                name="Public",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                name="Private",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                cidr_mask=20
            )
        ])

        for subnet in vpc.public_subnets:
            Tags.of(subnet).add('aws-cdk:subnet-type', 'Public')

        for subnet in vpc.private_subnets:
            Tags.of(subnet).add('aws-cdk:subnet-type', 'Private')

        cluster = ecs.Cluster(self, "LanPartyServers", vpc=vpc)

        CfnOutput(self, "VpcId", value=vpc.vpc_id, export_name="VpcId")
        CfnOutput(self, "LanPartyServersClusterName", value=cluster.cluster_name, export_name="LanPartyServersClusterName")
        CfnOutput(self, "PublicSubnetIds", value=",".join([subnet.subnet_id for subnet in vpc.public_subnets]), export_name="PublicSubnetIds")
        CfnOutput(self, "PrivateSubnetIds", value=",".join([subnet.subnet_id for subnet in vpc.private_subnets]), export_name="PrivateSubnetIds")
