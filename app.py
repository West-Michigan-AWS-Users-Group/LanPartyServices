import os
import subprocess
import aws_cdk as cdk

from lan_party_services.core.core import Core as core
from lan_party_services.nlb.nlb import Nlb as nlb
from lan_party_services.discord_bot.discord_bot import DiscordBot as discord_bot
from lan_party_services.info_mirror.info_mirror import info
from lan_party_services.quake3.quake3 import quake3
from lan_party_services.tee_worlds.teeworlds import teeworlds
from lan_party_services.ut2k4.ut2k4 import ut2k4
from lan_party_services.ut99.ut99 import ut99

# Execute the process_md_into_html.py script
subprocess.run(["python3", "process_md_into_html.py"], check=True)

# Upload assets to S3 - only needed one time prior to deployment. Copyrighted assets are not included in this repo,
# so you will need to provide them to work, ie, Quake, Unreal Tournament, Total Annihilation, etc.
# subprocess.run(['python3', 'upload_assets.py'], check=True)

# Set environment variables
account = os.getenv("AWS_ACCOUNT_NUMBER")
environment = "prod"
prefix = "lan-party-services"
template_bucket_name = f"{environment}-lan-party-services-cfn-templates"

env_us_east_1 = cdk.Environment(account=account, region="us-east-1")
env_us_east_2 = cdk.Environment(account=account, region="us-east-2")

app = cdk.App()

# Define stacks with the appropriate env parameter and prefix
info(app, f"{environment}-{prefix}-info", env=env_us_east_1)
core(app, f"{environment}-{prefix}-core", env=env_us_east_2)
nlb(app, f"{environment}-{prefix}-nlb", env=env_us_east_2)
quake3(app, f"{environment}-{prefix}-quake3", env=env_us_east_2)
ut99(app, f"{environment}-{prefix}-ut99", env=env_us_east_2)
ut2k4(app, f"{environment}-{prefix}-ut2k4", env=env_us_east_2)
teeworlds(app, f"{environment}-{prefix}-teeworlds", env=env_us_east_2)
discord_bot(app, f"{environment}-{prefix}-discord-bot", env=env_us_east_2)

app.synth()
