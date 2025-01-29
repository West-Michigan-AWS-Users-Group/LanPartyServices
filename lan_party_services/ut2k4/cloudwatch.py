import os
import re
from aws_cdk import Duration, aws_cloudwatch as cloudwatch, aws_logs as logs, aws_sns as sns, \
    aws_sns_subscriptions as subs, \
    aws_lambda as _lambda, \
    aws_iam as iam, \
    aws_sqs as sqs, \
    aws_lambda_event_sources as lambda_event_sources
from aws_cdk.aws_logs import FilterPattern
from aws_cdk import aws_cloudwatch_actions as cloudwatch_actions


def create_cloudwatch_resources(scope, stack_name, cluster, service, nlb, log_group):
    # Make the stack name ANSI compliant
    stack_name_ansi = re.sub(r'[^a-zA-Z0-9]', '', stack_name)

    # Create a CloudWatch dashboard
    dashboard = cloudwatch.Dashboard(scope, f"{stack_name_ansi}Dashboard",
                                     dashboard_name=f"{stack_name_ansi}PerformanceDashboard")

    # Individual container CPU usage widget
    cpu_usage_widget = cloudwatch.GraphWidget(
        title="Container CPU Usage",
        left=[cloudwatch.Metric(
            namespace="AWS/ECS",
            metric_name="CPUUtilization",
            dimensions_map={
                "ClusterName": cluster.cluster_name,
                "ServiceName": service.service_name
            },
            statistic="Average",
            period=Duration.minutes(1)
        )]
    )

    # Individual container memory usage widget
    memory_usage_widget = cloudwatch.GraphWidget(
        title="Container Memory Usage",
        left=[cloudwatch.Metric(
            namespace="AWS/ECS",
            metric_name="MemoryUtilization",
            dimensions_map={
                "ClusterName": cluster.cluster_name,
                "ServiceName": service.service_name
            },
            statistic="Average",
            period=Duration.minutes(1)
        )]
    )

    # NLB requests per minute widget
    nlb_requests_widget = cloudwatch.GraphWidget(
        title="NLB Requests Per Minute",
        left=[cloudwatch.Metric(
            namespace="AWS/NetworkELB",
            metric_name="RequestCount",
            dimensions_map={
                "LoadBalancer": nlb.load_balancer_arn
            },
            statistic="Sum",
            period=Duration.minutes(1)
        )]
    )

    # Number of healthy targets widget
    healthy_targets_widget = cloudwatch.GraphWidget(
        title="Healthy Targets",
        left=[cloudwatch.Metric(
            namespace="AWS/NetworkELB",
            metric_name="HealthyHostCount",
            dimensions_map={
                "LoadBalancer": nlb.load_balancer_arn
            },
            statistic="Average",
            period=Duration.minutes(1)
        )]
    )

    # Add widgets to the dashboard
    dashboard.add_widgets(cpu_usage_widget, memory_usage_widget, nlb_requests_widget, healthy_targets_widget)

    # Create an SNS topic for alerts
    topic = sns.Topic(scope, f"{stack_name_ansi}AlertsTopic")

    # Create an SQS queue
    queue = sqs.Queue(scope, f"{stack_name_ansi}AlertsQueue")

    # Subscribe the SQS queue to the SNS topic
    topic.add_subscription(subs.SqsSubscription(queue))

    # Create a Lambda function
    lambda_function = _lambda.Function(
        scope, f"{stack_name_ansi}DiscordWebhookLambda",
        runtime=_lambda.Runtime.PYTHON_3_11,
        handler="lambda_function.lambda_handler",
        code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'lambda')),
        # environment={
        #     'WEBHOOK_URL': webhook_url
        # }
    )

    # Grant the Lambda function permissions to read from the SQS queue
    queue.grant_consume_messages(lambda_function)

    # Add the SQS queue as an event source for the Lambda function
    lambda_function.add_event_source(lambda_event_sources.SqsEventSource(queue))

    # Create a policy for the Lambda function to access Secrets Manager
    lambda_function.add_to_role_policy(iam.PolicyStatement(
        actions=["secretsmanager:GetSecretValue"],
        resources=["*"]
    ))

    # Create a CloudWatch Logs subscription filter
    logs.SubscriptionFilter(scope, f"{stack_name_ansi}LogSubscriptionFilter",
                            log_group=log_group,
                            destination=logs.LogSubscriptionDestination.sqs(queue),
                            filter_pattern=FilterPattern.any_term("___New Player Joined -"))

    metric_filter = logs.MetricFilter(scope, f"{stack_name_ansi}LogFilter",
                                      log_group=log_group,
                                      metric_namespace=stack_name_ansi,
                                      # Example log "___New Player Joined - Player, 11.11.22.33:60318"
                                      metric_name="PlayerJoined",
                                      filter_pattern=FilterPattern.any_term("___New Player Joined -"),
                                      metric_value="1")
    # Create a CloudWatch alarm based on the metric filter
    # alarm = cloudwatch.Alarm(scope, f"{stack_name_ansi}PlayerJoinedAlarm",
    #                          metric=metric_filter.metric(),
    #                          threshold=1,
    #                          evaluation_periods=1,
    #                          datapoints_to_alarm=1,
    #                          treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING)

    # Add the SNS topic as an alarm action
    alarm.add_alarm_action(cloudwatch_actions.SnsAction(topic))
