import sys
import os
from aws_cdk import App
from aws_cdk.assertions import Template, Match

# Add the root directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lan_party_services.lan_party_services_stack import LanPartyServicesStack


def test_all_resources_have_service_tag():
    app = App()
    stack = LanPartyServicesStack(app, "lan-party-services")
    template = Template.from_stack(stack)

    # Iterate through all resources in the template
    for resource in template.to_json().get("Resources", {}).values():
        # Check if the resource has tags
        tags = resource.get("Properties", {}).get("Tags", [])
        # Assert that the 'service' tag is present with any value
        assert any(
            tag.get("Key") == "service" and tag.get("Value") is not None for tag in tags
        ), f"Resource {resource} does not have the 'service' tag with any value"
