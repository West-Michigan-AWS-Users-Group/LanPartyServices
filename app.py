#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lan_party_services.core import CoreStack
from lan_party_services.quake3 import Quake3

# Set environment variables
account = os.getenv("AWS_ACCOUNT_NUMBER")
region = 'us-east-2'

env = cdk.Environment(account=account, region=region)

app = cdk.App()
CoreStack(app, "CoreStack", env=env)
Quake3(app, "Quake3Stack", env=env)

app.synth()
