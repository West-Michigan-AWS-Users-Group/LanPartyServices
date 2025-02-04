import os
import boto3
import json
import logging

# Configure logging
logger = logging.getLogger()


def handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Check if queryStringParameters and stack_name are present in the event
    if (
        "queryStringParameters" not in event
        or "stack_name" not in event["queryStringParameters"]
    ):
        logger.error("Missing stack_name parameter")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing stack_name parameter"}),
        }

    stack_name = event["queryStringParameters"]["stack_name"]
    full_stack_name = os.environ["STACK_NAME_PREFIX"] + stack_name
    logger.info("Full stack name: %s", full_stack_name)

    ecs = boto3.client("ecs")

    # List all ECS clusters
    clusters_response = ecs.list_clusters()
    cluster_arns = clusters_response["clusterArns"]

    # Filter clusters containing the specified parameter
    filtered_clusters = [arn for arn in cluster_arns if 'core' in arn]

    # Check if any services in the filtered clusters contain the specified parameter
    for cluster_arn in filtered_clusters:
        logger.info("Checking cluster: %s", cluster_arn)
        services_response = ecs.list_services(cluster=cluster_arn)
        service_arns = services_response["serviceArns"]
        logger.info("Services in cluster %s: %s", cluster_arn, service_arns)
        filtered_services = [arn for arn in service_arns if stack_name in arn]
        logger.info("Filtered services in cluster %s: %s", cluster_arn, filtered_services)
        if filtered_services:
            logger.info("Found matching services in cluster %s", cluster_arn)
            return {
                "statusCode": 200,
                "body": json.dumps({"result": True}),
            }

    return {
        "statusCode": 200,
        "body": json.dumps({"result": False}),
    }
