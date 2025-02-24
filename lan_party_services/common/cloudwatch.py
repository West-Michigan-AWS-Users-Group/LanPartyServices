import os
import re
from typing import List

import aws_cdk.aws_logs_destinations as cloudwatch_destinations
from aws_cdk import (
    Duration,
    aws_cloudwatch as cloudwatch,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_ssm as ssm,
)
from aws_cdk.aws_logs import FilterPattern
from jinja2 import Environment, FileSystemLoader


def create_cloudwatch_resources(
    scope: object,
    stack_name: str,
    cluster: object,
    service: object,
    nlb: object,
    log_group: object,
    log_strings: List[str],
) -> None:
    """
    Create CloudWatch resources including a dashboard, widgets, and Lambda function used for sending webhooks.

    Args:
        scope (object): The scope in which to define this construct.
        stack_name (str): The name of the stack.
        cluster (object): The ECS cluster.
        service (object): The ECS service.
        nlb (object): The Network Load Balancer.
        log_group (object): The CloudWatch log group.
        log_strings (List[str]): List of strings to create subscription filters and metric filters.
    """
    # Split the stack name to derive the environment
    stack_name_parts = stack_name.split("-")
    environment = stack_name_parts[0]
    stack_name_s = stack_name_parts[-1].replace("-", "_")
    app_name = "-".join(stack_name_parts[1:-1]).replace("-", "_")

    stack_name_ansi = re.sub(r"[^a-zA-Z0-9]", "", "-".join(stack_name_parts[1:]))

    # Create a CloudWatch dashboard
    dashboard = cloudwatch.Dashboard(
        scope,
        f"{stack_name_ansi}Dashboard",
        dashboard_name=f"{stack_name_ansi}PerformanceDashboard",
    )

    # Individual container CPU usage widget
    cpu_usage_widget = cloudwatch.GraphWidget(
        title="Container CPU Usage",
        left=[
            cloudwatch.Metric(
                namespace="AWS/ECS",
                metric_name="CPUUtilization",
                dimensions_map={
                    "ClusterName": cluster.cluster_name,
                    "ServiceName": service.service_name,
                },
                statistic="Average",
                period=Duration.minutes(1),
            )
        ],
    )

    # Individual container memory usage widget
    memory_usage_widget = cloudwatch.GraphWidget(
        title="Container Memory Usage",
        left=[
            cloudwatch.Metric(
                namespace="AWS/ECS",
                metric_name="MemoryUtilization",
                dimensions_map={
                    "ClusterName": cluster.cluster_name,
                    "ServiceName": service.service_name,
                },
                statistic="Average",
                period=Duration.minutes(1),
            )
        ],
    )
    if nlb:
        # NLB requests per minute widget
        nlb_requests_widget = cloudwatch.GraphWidget(
            title="NLB Requests Per Minute",
            left=[
                cloudwatch.Metric(
                    namespace="AWS/NetworkELB",
                    metric_name="RequestCount",
                    dimensions_map={"LoadBalancer": nlb.load_balancer_arn},
                    statistic="Sum",
                    period=Duration.minutes(1),
                )
            ],
        )

        # Number of healthy targets widget
        healthy_targets_widget = cloudwatch.GraphWidget(
            title="Healthy Targets",
            left=[
                cloudwatch.Metric(
                    namespace="AWS/NetworkELB",
                    metric_name="HealthyHostCount",
                    dimensions_map={"LoadBalancer": nlb.load_balancer_arn},
                    statistic="Average",
                    period=Duration.minutes(1),
                )
            ],
        )

    if nlb:
        # Add widgets to the dashboard
        dashboard.add_widgets(
            cpu_usage_widget,
            memory_usage_widget,
            nlb_requests_widget,
            healthy_targets_widget,
        )

    # Define the SSM parameter path
    ssm_parameter_path = f"/{environment}/{app_name}/{stack_name_s}/discord_webhook_url"

    if stack_name_s != "bot":
        # Fetch the SSM parameter value
        discord_webhook_url = ssm.StringParameter.value_from_lookup(
            scope, ssm_parameter_path
        )

        # Determine the stack's folder path
        stack_webhook_module_path = os.path.join(
            os.path.dirname(__file__), "..", stack_name_s, "discord_webhook_lambda"
        )

        # Validate the presence of the directory
        os.makedirs(stack_webhook_module_path, exist_ok=True)

        # Add an __init__.py file to the directory
        init_file_path = os.path.join(stack_webhook_module_path, "__init__.py")
        open(init_file_path, "w").close()

        # Render the Jinja template
        env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "discord_webhook_lambda")
            )
        )
        template = env.get_template("lambda_function.py.j2")
        rendered_code = template.render(server_name=stack_name_s.capitalize())

        # Save the rendered code to a temporary file with a unique prefix
        temp_file_path = os.path.join(stack_webhook_module_path, f"lambda_function.py")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(rendered_code)

        # Create a Lambda function that can send webhook messages to a Discord channel
        lambda_function = _lambda.Function(
            scope,
            f"{stack_name_ansi}DiscordWebhookLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler=f"lambda_function.lambda_handler",
            code=_lambda.Code.from_asset(stack_webhook_module_path),
            environment={"DISCORD_WEBHOOK_URL": discord_webhook_url},
        )

        # Grant the Lambda function permissions to read from SSM Parameter Store
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[
                    f"arn:aws:ssm:{scope.region}:{scope.account}:parameter{ssm_parameter_path}"
                ],
            )
        )

    # Combine log strings into a single filter pattern
    if log_strings:
        combined_filter_pattern = FilterPattern.any_term(*log_strings)
        # Create a single CloudWatch Logs subscription filter with the combined pattern
        logs.SubscriptionFilter(
            scope,
            f"{stack_name_ansi}LogSubscriptionFilter",
            log_group=log_group,
            destination=cloudwatch_destinations.LambdaDestination(lambda_function),
            filter_pattern=combined_filter_pattern,
        )

        # Create individual metric filters for each log string
        for log_string in log_strings:
            log_string_ansi = re.sub(r"[^a-zA-Z0-9]", "", log_string)
            metric_name = re.sub(r"[:*$]", "_", f"{stack_name_s}_{log_string}")
            logs.MetricFilter(
                scope,
                f"{stack_name_ansi}Lf{log_string_ansi}Metric"[:64],
                log_group=log_group,
                metric_namespace=stack_name_ansi,
                metric_name=metric_name,
                filter_pattern=FilterPattern.any_term(log_string),
                metric_value="1",
            )
