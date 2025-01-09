from aws_cdk import (Duration, Fn, Stack, Tags, aws_ec2 as ec2, aws_ecr_assets as ecr_assets, aws_ecs as ecs,
                     aws_elasticloadbalancingv2 as elbv2, aws_iam as iam, aws_logs as logs, aws_route53 as route53,
                     aws_route53_targets as targets)
from constructs import Construct
import os

from lan_party_services.core import used_azs


class Quake3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # add tags
        Tags.of(self).add("service", "LanPartyServices")
        Tags.of(self).add("stack", self.__class__.__name__)

        vpc_id = Fn.import_value("VpcId")
        private_subnet_ids = Fn.import_value("PrivateSubnetIds").split(",")
        public_subnet_ids = Fn.import_value("PublicSubnetIds").split(",")
        private_route_table_ids = Fn.import_value("PrivateRouteTableIds").split(",")
        public_route_table_ids = Fn.import_value("PublicRouteTableIds").split(",")

        app_port = 27960
        health_check_port = 8080

        vpc = ec2.Vpc.from_vpc_attributes(self, "CoreVPC",
                                          vpc_id=vpc_id,
                                          availability_zones=used_azs['us-east-2'],
                                          private_subnet_ids=private_subnet_ids,
                                          public_subnet_ids=public_subnet_ids,
                                          private_subnet_route_table_ids=private_route_table_ids,
                                          public_subnet_route_table_ids=public_route_table_ids)

        cluster_name = Fn.import_value("LanPartyServersClusterName")
        cluster = ecs.Cluster.from_cluster_attributes(self, cluster_name,
                                                      cluster_name=cluster_name,
                                                      vpc=vpc)

        image = ecr_assets.DockerImageAsset(self, "Quake3Image",
                                            directory=os.path.join(os.path.dirname(__file__), "quake3"))

        # Import the security group for the NLB from the core stack
        nlb_tg_sg_id = Fn.import_value("NlbTgSGId")
        nlb_tg_security_group = ec2.SecurityGroup.from_security_group_id(self, "ImportedNlbTgSG", nlb_tg_sg_id)

        # Import the public network load balancer from corestack
        nlb_arn = Fn.import_value("PublicNLBArn")
        nlb_dns_name = Fn.import_value("PublicNLBDnsName")
        nlb_canonical_hosted_zone_id = Fn.import_value("PublicNLBCanonicalHostedZoneId")
        nlb = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(self, "ImportedNLB",
                                                                              load_balancer_arn=nlb_arn,
                                                                              vpc=vpc,
                                                                              load_balancer_canonical_hosted_zone_id=nlb_canonical_hosted_zone_id,
                                                                              load_balancer_dns_name=nlb_dns_name)

        # Create a log group with a 1-day retention policy
        log_group = logs.LogGroup(self, "Quake3LogGroup",
                                  retention=logs.RetentionDays.ONE_DAY)

        # Create an IAM role for the ECS task with permissions to write to CloudWatch Logs
        task_role = iam.Role(self, "Quake3TaskRole",
                             assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                             inline_policies={
                                 "CloudWatchLogsPolicy": iam.PolicyDocument(
                                     statements=[
                                         iam.PolicyStatement(
                                             actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                                             resources=[log_group.log_group_arn]
                                         )
                                     ]
                                 )
                             })

        # Create a Fargate service with a sidecar container for health checks
        task_definition = ecs.FargateTaskDefinition(self, "Quake3TaskDef",
                                                    task_role=task_role)

        # Sidecar container for health checks - uses busybox to respond to http requests
        health_check_container = task_definition.add_container("healthcheck",
                                                               image=ecs.ContainerImage.from_registry("busybox:latest"),
                                                               memory_limit_mib=128,
                                                               essential=True,
                                                               command=["sh", "-c",
                                                                        "while true; do { echo -e 'HTTP/1.1 200 OK\r\n'; echo 'ok'; } | nc -l -p 8080; done"])
        health_check_container.add_port_mappings(
            ecs.PortMapping(container_port=health_check_port, protocol=ecs.Protocol.TCP))

        # Main container
        main_container = task_definition.add_container("quake3-container",
                                                       image=ecs.ContainerImage.from_docker_image_asset(image),
                                                       memory_limit_mib=512,
                                                       logging=ecs.LogDriver.aws_logs(stream_prefix="Quake3",
                                                                                      log_group=log_group),
                                                       # Update commands here to switch server config.
                                                       # https://github.com/LacledesLAN/gamesvr-ioquake3
                                                       command=["/app/ioq3ded.x86_64",
                                                                "+set", "com_hunkmegs", "256",
                                                                "+set", "fs_game", "osp",
                                                                "+exec", "ffa-instagib.cfg",
                                                                "+exec", "playlists.cfg",
                                                                "+vstr", "stock-dm-1"])

        # Create the Fargate service
        service = ecs.FargateService(self, "Quake3Service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     desired_count=1,
                                     security_groups=[nlb_tg_security_group])

        main_container.add_port_mappings(ecs.PortMapping(container_port=app_port, protocol=ecs.Protocol.TCP))

        # Add SG rules to NLB in core stack
        nlb_tg_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(app_port),
                                               f"Allow TCP traffic on {app_port}")
        nlb_tg_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.udp(app_port),
                                               f"Allow UDP traffic on {app_port}")

        # Add a tcp/udp listener
        tcp_udp_listener = nlb.add_listener(f"TCPUDPListener{app_port}", port=app_port, protocol=elbv2.Protocol.TCP_UDP)
        tcp_udp_listener.add_targets(f"FargateServiceTargetTCPUDP{app_port}",
                                     port=app_port,
                                     protocol=elbv2.Protocol.TCP_UDP,
                                     targets=[service.load_balancer_target(
                                         container_name="quake3-container",
                                         container_port=app_port
                                     )],
                                     health_check=elbv2.HealthCheck(
                                         interval=Duration.seconds(15),
                                         timeout=Duration.seconds(10),
                                         healthy_threshold_count=2,
                                         unhealthy_threshold_count=2,
                                         port=str(health_check_port),
                                         protocol=elbv2.Protocol.TCP),
                                     deregistration_delay=Duration.seconds(0))

        # Add health check port to the security group
        nlb_tg_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(health_check_port),
                                               f"Allow TCP traffic on {health_check_port}")

        # Add a DNS record to the zone named grlanparty.info
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name="grlanparty.info")
        route53.ARecord(self, "Quake3AliasRecord",
                        record_name="quake3.grlanparty.info",
                        target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(nlb)),
                        zone=zone)
