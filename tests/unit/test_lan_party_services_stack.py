import aws_cdk as core
import aws_cdk.assertions as assertions

from lan_party_services.lan_party_services_stack import LanPartyServicesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lan_party_services/lan_party_services_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LanPartyServicesStack(app, "lan-party-services")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
