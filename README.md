# CDK app to deploy and run a number of video game servers for a LAN party

This app contains:
- Web front end for serving content for LAN attendees
- Unreal Tournament 99 server
- Quake 3 server
- Tee-worlds server
- Open-RA server

And information on other games where a server isn't required/supported.
- Starcraft: Brood War info


```
export AWS_ACCOUNT_NUMBER=<account-number>                                    
export AWS_REGION=us-east-1
export AWS_PROFILE=wmaug-member
export AWS_DEFAULT_PROFILE=wmaug-member
export CDK_DEFAULT_ACCOUNT=wmaug-member
export CDK_DEFAULT_REGION=us-east-1

$ cdk synth
cdk deploy --all
```
