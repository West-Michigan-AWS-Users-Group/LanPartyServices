import http.client
import json


def check_server_status(stack_name: str) -> bool:
    """Checks the server status from the API.

    Args:
        stack_name (str): The stack name to be checked.

    Returns:
        bool: True if the server is online, False otherwise.
    """
    # Set up the connection
    conn = http.client.HTTPSConnection("api.grlanparty.info")

    # Make the GET request
    conn.request("GET", f"/status?stack_name={stack_name}")

    # Get the response
    response = conn.getresponse()
    data = response.read()

    # Close the connection
    conn.close()

    # Parse the response
    if response.status == 200:
        result = json.loads(data).get("result", False)
        return result
    else:
        return False
