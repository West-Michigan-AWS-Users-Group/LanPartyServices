import os
import boto3
import datetime
from datetime import timedelta
import json


def handler(event, context):
    # Check if queryStringParameters and stack_name are present in the event
    if (
        "queryStringParameters" not in event
        or "stack_name" not in event["queryStringParameters"]
    ):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing stack_name parameter"}),
        }

    stack_name = event["queryStringParameters"]["stack_name"]
    full_stack_name = os.environ["STACK_NAME_PREFIX"] + stack_name

    cloudwatch = boto3.client("cloudwatch")
    ecs = boto3.client("ecs")

    # Query CloudWatch for the running task count metric
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/ECS",
        MetricName="RunningTaskCount",
        Dimensions=[{"Name": "ClusterName", "Value": full_stack_name}],
        StartTime=datetime.datetime.utcnow() - timedelta(minutes=5),
        EndTime=datetime.datetime.utcnow(),
        Period=300,
        Statistics=["Average"],
    )

    running_task_count = 0
    if response["Datapoints"]:
        running_task_count = response["Datapoints"][0]["Average"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"stack_name": stack_name, "running_task_count": running_task_count}
        ),
    }
