from os import path

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct
from aws_cdk.aws_ecr_assets import DockerImageAsset


class LanPartyServicesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)     # default is all AZs in region

        cluster = ecs.Cluster(self, "LanPartyServers", vpc=vpc)

        asset = DockerImageAsset(self, "MyBuildImage",
                                 directory=path.join(__dirname, "quake3")
                                 )

        fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(self, "MyFargateService",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=1,            # Default is 1
            task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                container_port=27015),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True)  # Default is True

        # Add port mappings
        container = fargate_service.task_definition.default_container
        container.add_port_mappings(
            ecs.PortMapping(container_port=27015, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27036, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27960, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27961, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27962, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27963, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27964, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27965, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27966, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27967, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27968, protocol=ecs.Protocol.TCP),
            ecs.PortMapping(container_port=27969, protocol=ecs.Protocol.TCP),
            # ecs.PortMapping(container_port=27015, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27031, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27032, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27033, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27034, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27035, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27036, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27960, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27961, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27962, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27963, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27964, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27965, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27966, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27967, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27968, protocol=ecs.Protocol.UDP),
            # ecs.PortMapping(container_port=27969, protocol=ecs.Protocol.UDP)
        )
