from aws_cdk import (Aws, CfnOutput, Duration, RemovalPolicy, Size, Stack, Tags,
                     aws_certificatemanager as certificatemanager,
                     aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_iam as iam,
                     aws_route53 as route53, aws_route53_targets as targets, aws_s3 as s3,
                     aws_s3_deployment as s3_deployment)
from constructs import Construct
import os
from lan_party_services.asset_paths import asset_file_paths

class info(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain_name: str = "grlanparty.info",
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        """
        Stack containing the resources for the grlanparty.info website to host server information and downloads.
        :param scope:
        :param construct_id:
        :param domain_name:
        :param kwargs:
        """
        app_group = self.__class__.__name__.capitalize()
        app_group_l = app_group.lower()
        Tags.of(self).add("service", app_group)
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=domain_name)
        # Copyrighted material, binaries or other large files that cannot be otherwise stored publicly in git
        account_number = os.getenv("AWS_ACCOUNT_NUMBER")
        asset_bucket_name = f"cdk-hnb659fds-assets-{account_number}-{Aws.REGION}"

        bucket = s3.Bucket(self, "bucket",
                           bucket_name=domain_name,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           public_read_access=False,
                           auto_delete_objects=True,
                           removal_policy=RemovalPolicy.DESTROY)

        cloudfront_oai = cloudfront.OriginAccessIdentity(self, "cloudfrontOai", comment=f"OAI for {construct_id}")

        bucket.grant_read(cloudfront_oai)
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[bucket.arn_for_objects("*")],
                principals=[
                    iam.CanonicalUserPrincipal(cloudfront_oai.cloud_front_origin_access_identity_s3_canonical_user_id)]
            )
        )

        certificate = certificatemanager.Certificate(self, "certificate",
                                                     domain_name=domain_name,
                                                     validation=certificatemanager.CertificateValidation.from_dns(zone),
                                                     subject_alternative_names=[f"www.{domain_name}"])

        redirect_function = cloudfront.Function(self, "redirectFunction",
                                                function_name="RedirectWWWToNonWWW",
                                                code=cloudfront.FunctionCode.from_inline(f"""
function handler(event) {{
    var request = event.request;
    request.headers["x-forwarded-host"] = request.headers["host"];
    if (request.headers["host"].value !== "{domain_name}") {{
        return {{
            statusCode: 301,
            statusDescription: "Moved Permanently",
            headers: {{
                location: {{
                    value: "https://{domain_name}/site/index.html" + request.uri
                }}
            }}
        }};
    }}
    return request;
}}
"""))

        my_response_headers_policy_website = cloudfront.ResponseHeadersPolicy(self, "myResponseHeadersPolicyWebsite",
                                                                              response_headers_policy_name="HostingPolicy",
                                                                              comment="Response Headers Policy",
                                                                              security_headers_behavior=cloudfront.ResponseSecurityHeadersBehavior(
                                                                                  content_type_options=cloudfront.ResponseHeadersContentTypeOptions(
                                                                                      override=True),
                                                                                  frame_options=cloudfront.ResponseHeadersFrameOptions(
                                                                                      frame_option=cloudfront.HeadersFrameOption.DENY,
                                                                                      override=True),
                                                                                  referrer_policy=cloudfront.ResponseHeadersReferrerPolicy(
                                                                                      referrer_policy=cloudfront.HeadersReferrerPolicy.ORIGIN,
                                                                                      override=True),
                                                                                  strict_transport_security=cloudfront.ResponseHeadersStrictTransportSecurity(
                                                                                      access_control_max_age=Duration.seconds(
                                                                                          31536000),  # 12 months
                                                                                      include_subdomains=True,
                                                                                      override=True),
                                                                                  xss_protection=cloudfront.ResponseHeadersXSSProtection(
                                                                                      protection=True,
                                                                                      mode_block=True,
                                                                                      override=True)
                                                                              ))

        s3_origin = origins.S3Origin(bucket, origin_access_identity=cloudfront_oai)

        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn],
                principals=[iam.AnyPrincipal()],
                effect=iam.Effect.DENY
            )
        )

        distribution = cloudfront.Distribution(self, "distribution",
                                       certificate=certificate,
                                       default_root_object="site/index.html",
                                       domain_names=[domain_name, f"www.{domain_name}"],
                                       minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
                                       error_responses=[
                                           cloudfront.ErrorResponse(
                                               http_status=403,
                                               response_http_status=403,
                                               response_page_path="site/error.html",
                                               ttl=Duration.minutes(30)
                                           )
                                       ],
                                       default_behavior=cloudfront.BehaviorOptions(
                                           origin=s3_origin,
                                           compress=True,
                                           function_associations=[
                                               cloudfront.FunctionAssociation(
                                                   function=redirect_function,
                                                   event_type=cloudfront.FunctionEventType.VIEWER_REQUEST
                                               )
                                           ],
                                           origin_request_policy=cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
                                           viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                           allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                                           cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                                           cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                                           response_headers_policy=my_response_headers_policy_website
                                       ),
                                       # additional_behaviors={
                                       #     "site/*": cloudfront.BehaviorOptions(
                                       #         origin=s3_origin,
                                       #         compress=True,
                                       #         function_associations=[
                                       #             cloudfront.FunctionAssociation(
                                       #                 function=redirect_function,
                                       #                 event_type=cloudfront.FunctionEventType.VIEWER_REQUEST
                                       #             )
                                       #         ],
                                       #         origin_request_policy=cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
                                       #         viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                       #         allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                                       #         cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                                       #         cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                                       #         response_headers_policy=my_response_headers_policy_website
                                       #     )
                                       # }
                                       )

        route53.ARecord(self, "SiteAliasRecord",
                        record_name=domain_name,
                        target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
                        zone=zone)

        route53.ARecord(self, "SiteAliasRecordWWW",
                        record_name=f"www.{domain_name}",
                        target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
                        zone=zone)

        # Deploy site contents to S3 bucket
        s3_deployment.BucketDeployment(self, "DeployWebsite",
                                       sources=[s3_deployment.Source.asset("./lan_party_services/info_mirror/site")],
                                       destination_bucket=bucket,
                                       destination_key_prefix="site/",
                                       distribution=distribution,
                                       distribution_paths=["/*"],
                                       retain_on_delete=True)

        asset_bucket = s3.Bucket.from_bucket_name(self, "AssetBucket",
                                                  asset_bucket_name)
        # Can't get this deployment to work. going to just upload manually.
        # prod-lan-party-services-info | 12/20 | 3:54:37 PM | CREATE_FAILED        | Custom::CDKBucketDeployment
        # | Deploytotal_annihilation_total_annihilation__commander_pack_en_1_3_15733_pkg_zip/CustomResource-1024Mi
        # B-6144MiB/Default (Deploytotalannihilationtotalannihilationcommanderpacken1315733pkgzipCustomResource1024Mi
        # B6144MiB91524526) Received response status [FAILED] from custom resource. Message returned: [Errno 28] No s
        # pace left on device (RequestId: efd8e68d-8b09-44bf-9b4c-8199fcfc8ce8)
        # for file_path, prefix in asset_file_paths:
        #     zip_file_path = f"{file_path}.zip" if not file_path.endswith('.zip') else file_path
        #     s3_deployment.BucketDeployment(self, f"Deploy{zip_file_path.replace('/', '_').replace('.', '_')}",
        #                                    sources=[s3_deployment.Source.bucket(
        #                                        bucket=asset_bucket,
        #                                        zip_object_key=zip_file_path)],
        #                                    destination_bucket=bucket,
        #                                    destination_key_prefix=prefix,
        #                                    distribution=distribution,
        #                                    distribution_paths=[f"/{zip_file_path}"],
        #                                    memory_limit=1024,
        #                                    ephemeral_storage_size=Size.gibibytes(6))

        CfnOutput(self, "websiteUrl", value=f"https://{domain_name}")
