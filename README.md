# LAN Party Services
AWS CDK app to deploy and run a web server and number of video game servers for a LAN party.


![diagram.png](diagram.png)

This app contains:
- Web front end for serving content for LAN attendees - Hosted on Cloudfront backed by S3. 
This app dynamically generates documentation from each app's readme file for simple templated renderings of info pages.
- API Gateway for querying the status of each game server - Hosted on API Gateway backed by Lambda.
- Discord bot for querying the status of each game server, and starting and stopping of them - Hosted on ECS
- Cloudwatch log filters and discord alerts for certain games - used to notify of server events.

Game Servers:
- Open-RA server
- Quake 3 server (minus pak0.pk3 copyrighted material)
- Tee-worlds server
- Unreal Tournament 2004 server
- Unreal Tournament 99 server (minus maps, music sounds and texture copyrighted material)

Game Files/Info:
- Beyond All Reason (BAR)
- Starcraft: Brood War
- Total Annihilation
- Warhammer 40k: Speed Freeks

## Requirements
- AWS Account + Profile configured
- Python venv
- CDK bootstrapped environment

1. Set up a bunch of environment variables for the CDK app to use. 
```bash
export AWS_ACCOUNT_NUMBER=<account-number>                                    
export AWS_PROFILE=<profile-name>       
export AWS_DEFAULT_PROFILE=<profile-name>     
export CDK_DEFAULT_ACCOUNT=<profile-name>     
unset CDK_DEFAULT_REGION
unset AWS_REGION
```

2. Create a python virtual environment and install the required packages:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Obtain all the necessary files as outlined in `lan_party_services/asset_paths.py`. See each respective app README for
links or more information.

4. Login to AWS SSO (if using AWS SSO):
```bash
aws sso login --profile <profile>
```
5. synth and deploy the CDK app:
```bash
$ cdk synth
$ cdk deploy --all # or
$ cdk deploy <stack-name> # prod-lan-party-services-info | prod-lan-party-services-core | prod-lan-party-services-quake3 | etc. See app.py for stack names
```

6. Upload copyrighted/large assets to CDN bucket. These files are required for the game servers to run or for people to play and should not be stored in git.
```bash
python3 ./upload_assets.py
```
