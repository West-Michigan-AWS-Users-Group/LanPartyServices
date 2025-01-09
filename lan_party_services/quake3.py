from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
    Fn,
    Tags
)
from constructs import Construct
from lan_party_services.core import used_azs
import os

class Quake3(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # add tags
        Tags.of(self).add("service", "LanPartyServices")
        Tags.of(self).add("stack", self.__class__.__name__)

        vpc_id = Fn.import_value("VpcId")
        private_subnet_ids = Fn.import_value("PrivateSubnetIds").split(",")
        public_subnet_ids = Fn.import_value("PrivateSubnetIds").split(",")

        vpc = ec2.Vpc.from_vpc_attributes(self, "CoreVPC",
                                          vpc_id=vpc_id,
                                          availability_zones=used_azs['us-east-2'],
                                          private_subnet_ids=private_subnet_ids,
                                          public_subnet_ids=public_subnet_ids)

        cluster_name = Fn.import_value("LanPartyServersClusterName")
        cluster = ecs.Cluster.from_cluster_attributes(self, cluster_name,
                                                      cluster_name=cluster_name,
                                                      vpc=vpc)

        image = ecr_assets.DockerImageAsset(self, "Quake3Image",
                                            directory=os.path.join(os.path.dirname(__file__), "quake3"))

        service = ecs_patterns.NetworkLoadBalancedFargateService(self, "Quake3Service",
                                                                 cluster=cluster,
                                                                 cpu=256,
                                                                 desired_count=1,
                                                                 task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                                                                     image=ecs.ContainerImage.from_docker_image_asset(image),
                                                                     container_port=27960),
                                                                 memory_limit_mib=512,
                                                                 public_load_balancer=True)

        # Add port mappings
        container = service.task_definition.default_container
        container.add_port_mappings(
            ecs.PortMapping(container_port=27960, protocol=ecs.Protocol.UDP)
        )
