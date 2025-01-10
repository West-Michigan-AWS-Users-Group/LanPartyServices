import os

from aws_cdk import (Duration, Fn, Stack, Tags, aws_ec2 as ec2, aws_ecr_assets as ecr_assets, aws_ecs as ecs,
                     aws_elasticloadbalancingv2 as elbv2, aws_iam as iam, aws_logs as logs, aws_route53 as route53,
                     aws_route53_targets as targets)
from constructs import Construct

from lan_party_services.core.core import used_azs


class ut99(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app_group = self.__class__.__name__.capitalize()
        app_group_l = app_group.lower()
        Tags.of(self).add("service", app_group)

        ### Core stack imports
        vpc_id = Fn.import_value("VpcId")
        private_subnet_ids = Fn.import_value("PrivateSubnetIds").split(",")
        public_subnet_ids = Fn.import_value("PublicSubnetIds").split(",")
        private_route_table_ids = Fn.import_value("PrivateRouteTableIds").split(",")
        public_route_table_ids = Fn.import_value("PublicRouteTableIds").split(",")
        vpc = ec2.Vpc.from_vpc_attributes(self, "CoreVPC",
                                          vpc_id=vpc_id,
                                          availability_zones=used_azs['us-east-2'],
                                          private_subnet_ids=private_subnet_ids,
                                          public_subnet_ids=public_subnet_ids,
                                          private_subnet_route_table_ids=private_route_table_ids,
                                          public_subnet_route_table_ids=public_route_table_ids)
        # Cluster
        cluster_name = Fn.import_value("LanPartyServersClusterName")
        cluster = ecs.Cluster.from_cluster_attributes(self, cluster_name,
                                                      cluster_name=cluster_name,
                                                      vpc=vpc)
        # NLB
        nlb_tg_sg_id = Fn.import_value("NlbTgSGId")
        nlb_tg_security_group = ec2.SecurityGroup.from_security_group_id(self, "ImportedNlbTgSG", nlb_tg_sg_id)
        nlb_arn = Fn.import_value("PublicNLBArn")
        nlb_dns_name = Fn.import_value("PublicNLBDnsName")
        nlb_canonical_hosted_zone_id = Fn.import_value("PublicNLBCanonicalHostedZoneId")
        nlb = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(self, "ImportedNLB",
                                                                              load_balancer_arn=nlb_arn,
                                                                              vpc=vpc,
                                                                              load_balancer_canonical_hosted_zone_id=nlb_canonical_hosted_zone_id,
                                                                              load_balancer_dns_name=nlb_dns_name)

        ### Server config -
        #     Botpack mutators: https://wiki.unrealadmin.org/List_of_Gametypes_and_Mutators_%28UT%29
        instagib_ctf_face = "CTF-Face?game=BotPack.CTFGame?mutator=BotPack.InstaGibDM,MVES.MapVote,FlagAnnouncementsV2.FlagAnnouncements"
        ffa_vanilla = "DM-Deck16?game=BotPack.DeathMatchPlus?mutator=MVES.MapVote"
        # Rocket arena, deck-16][ has a weird name.
        ffa_rocket_arena = "DM-Deck16][?game=BotPack.DeathMatchPlus?mutator=BotPack.RocketArena"
        server_start_command = ffa_rocket_arena
        # Networking
        app_ports = [7777, 7778, 7779, 7780, 7781]
        health_check_port = 8080
        server_url = f"{app_group_l}.grlanparty.info"
        # Image
        image = ecr_assets.DockerImageAsset(self, f"{app_group}Image",
                                            directory=os.path.join(os.path.dirname(__file__), '..', app_group_l))
        # Logging
        log_group = logs.LogGroup(self, f"{app_group}LogGroup",
                                  retention=logs.RetentionDays.ONE_DAY)

        # Permissions
        task_role = iam.Role(self, f"{app_group}TaskRole",
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
        task_definition = ecs.FargateTaskDefinition(self, f"{app_group}TaskDef",
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
        main_container = task_definition.add_container(f"{app_group_l}-container",
                                                       image=ecs.ContainerImage.from_docker_image_asset(image),
                                                       memory_limit_mib=256,
                                                       logging=ecs.LogDriver.aws_logs(stream_prefix=app_group,
                                                                                      log_group=log_group),
                                                       environment={
                                                           "UT_SERVERURL": server_start_command,
                                                           "UT_SERVERNAME": server_url,
                                                           "UT_ADMINNAME": "",
                                                           "UT_ADMINEMAIL": "",
                                                           "UT_MOTD1": "Welcome to the GR LAN Party!",
                                                           "UT_DOUPLINK": "true",
                                                           "UT_ADMINPWD": "admin",
                                                           "UT_GAMEPWD": "",
                                                           "UT_WEBADMINUSER": "",
                                                           "UT_WEBADMINPWD": "",
                                                           "UT_MINPLAYERS_DM": "1",
                                                           "UT_MINPLAYERS_CTF": "1",
                                                           "UT_MAXPLAYERS": "16",
                                                           "UT_INITIALBOTS_DM": "2",
                                                           "UT_INITIALBOTS_CTF": "2"
                                                       })

        # Create the Fargate service
        service = ecs.FargateService(self, f"{app_group}Service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     desired_count=1,
                                     security_groups=[nlb_tg_security_group])
        for app_port in app_ports:
            main_container.add_port_mappings(ecs.PortMapping(container_port=app_port, protocol=ecs.Protocol.UDP))

            # Add SG rules to NLB in core stack
            nlb_tg_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.udp(app_port),
                                                   f"Allow UDP traffic on {app_port}")

            # Add udp listener
            udp_listener = nlb.add_listener(f"UDPListener{app_port}", port=app_port, protocol=elbv2.Protocol.UDP)
            udp_listener.add_targets(f"FargateServiceTargetUDP{app_port}",
                                     port=app_port,
                                     protocol=elbv2.Protocol.UDP,
                                     targets=[service.load_balancer_target(
                                         container_name=f"{app_group_l}-container",
                                         container_port=app_port,
                                         protocol=ecs.Protocol.UDP
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
        route53.ARecord(self, f"{app_group}AliasRecord",
                        record_name=server_url,
                        target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(nlb)),
                        zone=zone)
