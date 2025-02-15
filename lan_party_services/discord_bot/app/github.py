import http.client
import json
import os


def start_adhoc_workflow(stack_name_function_arg: str, workflow: str) -> str:
    """Starts an ad-hoc workflow on GitHub Actions.

    Args:
        stack_name_function_arg (str): The stack name to be used in the workflow.
        workflow (str): The workflow file to be triggered.

    Returns:
        str: The response from the GitHub API.
    """
    # Set up the connection
    conn = http.client.HTTPSConnection("api.github.com")

    # Set up the headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_API_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Create the payload
    payload = json.dumps({"ref": "main", "inputs": {"stack": stack_name_function_arg}})

    # Make the POST request
    conn.request(
        "POST",
        f"/repos/West-Michigan-AWS-Users-Group/LanPartyServices/actions/workflows/{workflow}/dispatches",
        body=payload,
        headers=headers,
    )

    # Get the response
    response = conn.getresponse()
    data = response.read()

    # Close the connection
    conn.close()

    return data.decode("utf-8")
