from aws_cdk import (
    Stack,
    aws_iam as iam,
    Tags,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
)
from constructs import Construct


class ApiGateway(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str = "grlanparty.info",
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        stack_name_ansi = (
            self.__class__.__name__.replace("-", "")
            .replace("_", "")
            .replace(".", "")
            .capitalize()
        )

        stack_name_parts = self.stack_name.split("-")
        environment = stack_name_parts[0]
        app_group = stack_name_ansi
        app_group_l = app_group.lower()
        # add tags
        Tags.of(self).add("service", app_group)

        # Define the Lambda function
        lambda_function = _lambda.Function(
            self,
            "GetStatus",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="status_lambda.handler",
            code=_lambda.Code.from_asset("lan_party_services/api/app/status"),
            environment={"STACK_NAME_PREFIX": f"{environment}-lan-party-services-"},
        )

        # Attach IAM policy to allow reading ECS clusters and services
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ecs:Describe*", "ecs:List*"],
                resources=["*"],
            )
        )

        # Set log retention policy to 1 day
        logs.LogGroup(
            self,
            "GetStatusLogGroup",
            log_group_name=f"/aws/lambda/{lambda_function.function_name}",
            retention=logs.RetentionDays.ONE_DAY,
        )

        # Define the API Gateway
        api = apigateway.RestApi(
            self,
            "Status",
            rest_api_name="Status Service",
            description="This service returns status of ECS tasks. (True, False)",
            default_cors_preflight_options={
                "allow_origins": ["https://grlanparty.info", "http://localhost"],
                "allow_methods": apigateway.Cors.ALL_METHODS,
            },
        )

        # Define the /status resource
        status = api.root.add_resource("status")
        status.add_method("GET", apigateway.LambdaIntegration(lambda_function))

        # Create a custom domain for the API Gateway
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=domain_name
        )
        certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name=f"api.{domain_name}",
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        custom_domain_name = apigateway.DomainName(
            self,
            "CustomDomain",
            domain_name=f"api.{domain_name}",
            certificate=certificate,
        )

        # Map the custom domain to the API Gateway
        apigateway.BasePathMapping(
            self,
            "BasePathMapping",
            domain_name=custom_domain_name,
            rest_api=api,
            base_path="",
        )

        # Create a DNS record for the custom domain
        route53.ARecord(
            self,
            "CustomDomainAliasRecord",
            record_name=f"api.{domain_name}",
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayDomain(custom_domain_name)
            ),
            zone=hosted_zone,
        )
