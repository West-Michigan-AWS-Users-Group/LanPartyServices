## API Gateway
This simple API gateway is used to determine if a stack is running or not. It does this by querying cloudwatch metrics
based on stack-name.

The stack name is passed with the short stack name, and not the prefix-app name.

Example test curl:
```bash
curl -X GET "https://api.grlanparty.info/status?stack_name=quake3"  
```
