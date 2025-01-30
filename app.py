import os
import subprocess
import boto3
import aws_cdk as cdk

from lan_party_services.core.core import core
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
quake3(app, f"{environment}-{prefix}-quake3", env=env_us_east_2)
ut99(app, f"{environment}-{prefix}-ut99", env=env_us_east_2)
ut2k4(app, f"{environment}-{prefix}-ut2k4", env=env_us_east_2)
teeworlds(app, f"{environment}-{prefix}-teeworlds", env=env_us_east_2)

app.synth()


# Add the
def bucket_exists(bucket_name):
    s3_client = boto3.client("s3")
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except boto3.exceptions.botocore.client.ClientError:
        return False


def upload_templates_to_s3(bucket_name):
    if bucket_exists(bucket_name):
        s3_client = boto3.client("s3")
        cdk_out_dir = "./cdk.out"

        for root, dirs, files in os.walk(cdk_out_dir):
            for file in files:
                if file.endswith("template.json"):
                    file_path = os.path.join(root, file)
                    s3_key = os.path.relpath(file_path, cdk_out_dir)
                    s3_client.upload_file(file_path, bucket_name, s3_key)
                    print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    else:
        print(f"Bucket {bucket_name} does not exist. Skipping upload.")


upload_templates_to_s3(template_bucket_name)
