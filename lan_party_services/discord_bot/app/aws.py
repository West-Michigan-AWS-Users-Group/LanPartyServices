import boto3


def check_stacks_exist(stack_names: list) -> bool:
    """Checks if the specified AWS CloudFormation stacks exist.

    Args:
        stack_names (list): A list of stack names to check.

    Returns:
        bool: True if all stacks exist, False otherwise.
    """
    cf_client = boto3.client("cloudformation")

    for stack_name in stack_names:
        try:
            response = cf_client.describe_stacks(StackName=f'prod-lan-party-services-{stack_name}')
            if not response["Stacks"]:
                return False
        except cf_client.exceptions.ClientError:
            return False

    return True
