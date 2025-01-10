from aws_cdk import (CfnOutput, Duration, RemovalPolicy, Stack, aws_certificatemanager as certificatemanager,
                     aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_iam as iam,
                     aws_route53 as route53, aws_route53_targets as targets, aws_s3 as s3,
                     aws_s3_deployment as s3_deployment)
from constructs import Construct


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
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=domain_name)
        # Copyrighted material, binaries or other large files that cannot be otherwise stored publicly in git
        asset_bucket = 'cdk-hnb659fds-assets-145023128664-us-east-2'

        cloudfront_oai = cloudfront.OriginAccessIdentity(self, "cloudfrontOai", comment=f"OAI for {construct_id}")

        bucket = s3.Bucket(self, "bucket",
                           bucket_name=domain_name,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           public_read_access=False,
                           auto_delete_objects=True,
                           removal_policy=RemovalPolicy.DESTROY)

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
                    value: "https://{domain_name}" + request.uri
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

        s3origin = origins.S3Origin(bucket, origin_access_identity=cloudfront_oai)

        distribution = cloudfront.Distribution(self, "distribution",
                                               certificate=certificate,
                                               default_root_object="index.html",
                                               domain_names=[domain_name, f"www.{domain_name}"],
                                               minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
                                               error_responses=[
                                                   cloudfront.ErrorResponse(
                                                       http_status=403,
                                                       response_http_status=403,
                                                       response_page_path="/error.html",
                                                       ttl=Duration.minutes(30)
                                                   )
                                               ],
                                               default_behavior=cloudfront.BehaviorOptions(
                                                   origin=s3origin,
                                                   compress=True,
                                                   function_associations=[
                                                       cloudfront.FunctionAssociation(
                                                           function=redirect_function,
                                                           event_type=cloudfront.FunctionEventType.VIEWER_REQUEST
                                                       )
                                                   ]
                                               ),
                                               additional_behaviors={
                                                   "/index.html": cloudfront.BehaviorOptions(
                                                       origin=s3origin,
                                                       response_headers_policy=my_response_headers_policy_website,
                                                       viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                       allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                                                       function_associations=[
                                                           cloudfront.FunctionAssociation(
                                                               function=redirect_function,
                                                               event_type=cloudfront.FunctionEventType.VIEWER_REQUEST
                                                           )
                                                       ]
                                                   )
                                               })

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
                                       sources=[s3_deployment.Source.asset("./lan_party_services/info_mirror")],
                                       destination_bucket=bucket,
                                       distribution=distribution,
                                       distribution_paths=["/*"])

        asset_file_paths = [
            ("total_annihiliation/setup_total_annihilation_commander_pack_3.1_(22139).exe", "total_annihiliation"),
            ("total_annihiliation/total_annihilation__commander_pack_en_1_3_15733.pkg", "total_annihiliation"),
            ("quake3/baseq3/pak0.pk3", "quake3/baseq3")
        ]

        for file_path, prefix in asset_file_paths:
            s3_deployment.BucketDeployment(self, f"Deploy{file_path.replace('/', '_').replace('.', '_')}",
                                           sources=[s3_deployment.Source.bucket(bucket_name=asset_bucket, object_key=file_path)],
                                           destination_bucket=bucket,
                                           destination_key_prefix=prefix,
                                           distribution=distribution,
                                           distribution_paths=[f"/{file_path}"])

        CfnOutput(self, "websiteUrl", value=f"https://{domain_name}")
