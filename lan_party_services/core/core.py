from aws_cdk import (CfnOutput, Stack, Tags, aws_ec2 as ec2, aws_ecs as ecs, aws_elasticloadbalancingv2 as elbv2)
from constructs import Construct

used_azs = {
    'us-east-2': ['us-east-2a']
}


class core(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # add tags
        Tags.of(self).add("service", self.__class__.__name__)

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

        # Create a security group for the NLB target group
        nlb_tg_security_group = ec2.SecurityGroup(self, "NlbTgSG",
                                                  vpc=vpc,
                                                  description="Allow all traffic from self",
                                                  allow_all_outbound=True)

        # Create a public network load balancer
        nlb = elbv2.NetworkLoadBalancer(self, "PublicNLB",
                                        vpc=vpc,
                                        internet_facing=True,
                                        security_groups=[nlb_tg_security_group])

        # Add a self-referencing rule to allow all traffic
        nlb_tg_security_group.add_ingress_rule(peer=nlb_tg_security_group, connection=ec2.Port.all_traffic())

        CfnOutput(self, "VpcId", value=vpc.vpc_id, export_name="VpcId")
        CfnOutput(self, "LanPartyServersClusterName", value=cluster.cluster_name,
                  export_name="LanPartyServersClusterName")
        CfnOutput(self, "PublicSubnetIds", value=",".join([subnet.subnet_id for subnet in vpc.public_subnets]),
                  export_name="PublicSubnetIds")
        CfnOutput(self, "PrivateSubnetIds", value=",".join([subnet.subnet_id for subnet in vpc.private_subnets]),
                  export_name="PrivateSubnetIds")
        CfnOutput(self, "PublicNLBArn", value=nlb.load_balancer_arn, export_name="PublicNLBArn")
        CfnOutput(self, "NlbTgSGId", value=nlb_tg_security_group.security_group_id, export_name="NlbTgSGId")
        CfnOutput(self, "PublicNLBDnsName", value=nlb.load_balancer_dns_name, export_name="PublicNLBDnsName")
        CfnOutput(self, "PublicNLBCanonicalHostedZoneId", value=nlb.load_balancer_canonical_hosted_zone_id,
                  export_name="PublicNLBCanonicalHostedZoneId")

        # Export route table IDs
        CfnOutput(self, "PublicRouteTableIds",
                  value=",".join([subnet.route_table.route_table_id for subnet in vpc.public_subnets]),
                  export_name="PublicRouteTableIds")
        CfnOutput(self, "PrivateRouteTableIds",
                  value=",".join([subnet.route_table.route_table_id for subnet in vpc.private_subnets]),
                  export_name="PrivateRouteTableIds")
