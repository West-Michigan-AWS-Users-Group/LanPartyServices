#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lan_party_services.core import CoreStack
from lan_party_services.info_mirror import GrLanPartyInfoStack
from lan_party_services.quake3 import Quake3Stack

# Set environment variables
account = os.getenv("AWS_ACCOUNT_NUMBER")

env_us_east_1 = cdk.Environment(account=account, region='us-east-1')
env_us_east_2 = cdk.Environment(account=account, region='us-east-2')

app = cdk.App()

# Define stacks with the appropriate env parameter
GrLanPartyInfoStack(app, "GrLanPartyInfoStack", env=env_us_east_1)
CoreStack(app, "CoreStack", env=env_us_east_2)
Quake3Stack(app, "Quake3Stack", env=env_us_east_2)

app.synth()
