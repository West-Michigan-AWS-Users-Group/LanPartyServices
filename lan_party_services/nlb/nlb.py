from aws_cdk import (
    CfnOutput,
    Fn,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct
from lan_party_services.core.core import used_azs


class Nlb(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        stack_name_ansi = (
            self.__class__.__name__.replace("-", "")
            .replace("_", "")
            .replace(".", "")
            .capitalize()
        )
        environment = self.node.try_get_context("environment")
        vpc_stack_name_ansi = f"{environment}Core".replace("-", "").replace("_", "").replace(".", "").capitalize()

        vpc_id = Fn.import_value(f"{vpc_stack_name_ansi}VpcId")
        public_subnet_ids = Fn.import_value(f"{vpc_stack_name_ansi}PublicSubnetIds").split(",")
        private_subnet_ids = Fn.import_value(f"{vpc_stack_name_ansi}PrivateSubnetIds").split(",")
        public_route_table_ids = Fn.import_value(f"{vpc_stack_name_ansi}PublicRouteTableIds").split(",")
        private_route_table_ids = Fn.import_value(f"{vpc_stack_name_ansi}PrivateRouteTableIds").split(",")

        vpc = ec2.Vpc.from_vpc_attributes(
            self,
            f"{environment}{vpc_stack_name_ansi}CoreVPC",
            vpc_id=vpc_id,
            availability_zones=used_azs["us-east-2"],
            public_subnet_ids=public_subnet_ids,
            private_subnet_ids=private_subnet_ids,
            public_subnet_route_table_ids=public_route_table_ids,
            private_subnet_route_table_ids=private_route_table_ids,
        )

        # Create a security group for the NLB target group
        nlb_tg_security_group = ec2.SecurityGroup(
            self,
            f"{environment}{stack_name_ansi}NlbTgSG",
            vpc=vpc,
            description="Allow all traffic from self",
            allow_all_outbound=True,
        )

        # Create a public network load balancer
        nlb = elbv2.NetworkLoadBalancer(
            self,
            f"{environment}{stack_name_ansi}PublicNLB",
            vpc=vpc,
            internet_facing=True,
            security_groups=[nlb_tg_security_group],
        )

        # Add a self-referencing rule to allow all traffic
        nlb_tg_security_group.add_ingress_rule(
            peer=nlb_tg_security_group, connection=ec2.Port.all_traffic()
        )

        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicNLBArn",
            value=nlb.load_balancer_arn,
            export_name=f"{environment}{stack_name_ansi}PublicNLBArn",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}NlbTgSGId",
            value=nlb_tg_security_group.security_group_id,
            export_name=f"{environment}{stack_name_ansi}NlbTgSGId",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicNLBDnsName",
            value=nlb.load_balancer_dns_name,
            export_name=f"{environment}{stack_name_ansi}PublicNLBDnsName",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicNLBCanonicalHostedZoneId",
            value=nlb.load_balancer_canonical_hosted_zone_id,
            export_name=f"{environment}{stack_name_ansi}PublicNLBCanonicalHostedZoneId",
        )
        CfnOutput(
            self,
            f"{environment}{stack_name_ansi}PublicNLBFullName",
            value=nlb.load_balancer_full_name,
            export_name=f"{environment}{stack_name_ansi}PublicNLBFullName",
        )
