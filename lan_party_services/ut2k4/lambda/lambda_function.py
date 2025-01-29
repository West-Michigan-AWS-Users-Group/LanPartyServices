import os
import json
import urllib3

http = urllib3.PoolManager()


def lambda_handler(event, context):
    webhook_url = 'https://canary.discord.com/api/webhooks/1334127928706994248/8tCtJ17nmOxP6bI-dVhH3C0Hh71xSydbGr-94H8Igm959rPHjew6ilYMJ4qplXP3RLp_'
    # webhook_url = os.environ['WEBHOOK_URL']

    # Extract the log message from the event
    for record in event['Records']:
        message = record['body']

        # Prepare the message payload
        msg = {
            'username': 'AWS BOT',
            'content': f'An alarm has been triggered: {message}'
        }
        headers = {'Content-Type': 'application/json'}

        # Send the message to the Discord webhook
        response = http.request(
            'POST',
            webhook_url,
            body=json.dumps(msg),
            headers=headers,
            retries=False
        )

        print(response.status)
        print(response.data)

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Discord!')
    }
