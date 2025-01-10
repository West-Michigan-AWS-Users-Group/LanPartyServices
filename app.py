#!/usr/bin/env python3
import os
import subprocess

import aws_cdk as cdk

from lan_party_services.core.core import core
from lan_party_services.info_mirror.info_mirror import info
from lan_party_services.quake3.quake3 import quake3
from lan_party_services.ut99.ut99 import ut99
from lan_party_services.tee_worlds.teeworlds import teeworlds

# Execute the process_md_into_html.py script
subprocess.run(['python3', 'process_md_into_html.py'], check=True)

# Upload assets to S3 - only needed one time prior to deployment. Copyrighted assets are not included in this repo,
# so you will need to provide them to work, ie, Quake, Unreal Tournament, Total Annihilation, etc.
# subprocess.run(['python3', 'upload_assets.py'], check=True)

# Set environment variables
account = os.getenv("AWS_ACCOUNT_NUMBER")

env_us_east_1 = cdk.Environment(account=account, region='us-east-1')
env_us_east_2 = cdk.Environment(account=account, region='us-east-2')

app = cdk.App()

# Define stacks with the appropriate env parameter
info(app, "info", env=env_us_east_1)
core(app, "core", env=env_us_east_2)
quake3(app, "quake3", env=env_us_east_2)
ut99(app, "ut99", env=env_us_east_2)
teeworlds(app, "teeworlds", env=env_us_east_2)

app.synth()
