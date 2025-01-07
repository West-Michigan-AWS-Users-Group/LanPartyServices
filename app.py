#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lan_party_services.lan_party_services_stack import LanPartyServicesStack

app = cdk.App()
LanPartyServicesStack(app, "LanPartyServicesStack",
                      env=cdk.Environment(
                          account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
                      ))

app.synth()
