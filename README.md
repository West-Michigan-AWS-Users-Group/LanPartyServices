# CDK app to deploy and run a number of video game servers for a LAN party

This app contains:
- Web front end for serving content for LAN attendees

Game Servers:
- Descent 3
- Unreal Tournament 99 server (minus maps, music sounds and texture copyrighted material)
- Unreal Tournament 2004 server
- Quake 3 server (minus pak0.pk3 copyrighted material)
- Tee-worlds server
- Open-RA server

Game Files/Info:
- Starcraft: Brood War
- Total Annihilation


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
