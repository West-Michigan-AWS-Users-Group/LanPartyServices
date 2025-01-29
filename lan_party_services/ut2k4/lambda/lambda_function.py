import os
import json
import urllib3
import logging

http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    webhook_url = 'https://canary.discord.com/api/webhooks/1334127928706994248/8tCtJ17nmOxP6bI-dVhH3C0Hh71xSydbGr-94H8Igm959rPHjew6ilYMJ4qplXP3RLp_'
    # webhook_url = os.environ['WEBHOOK_URL']

    for record in event['Records']:
        # Extract the log message from the SQS message
        sqs_message = json.loads(record['body'])
        log_message = json.loads(sqs_message['Message'])

        # Extract the actual log message
        message = log_message['logEvents'][0]['message']

        logger.info(f'Log message: {message}')

        # Prepare the message payload
        msg = {
            'username': 'UT2k4 Server Bot',
            'content': f'{message}'
        }
        logger.info(f'Log msg: {msg}')
        headers = {'Content-Type': 'application/json'}

        # Send the message to the Discord webhook
        response = http.request(
            'POST',
            webhook_url,
            body=json.dumps(msg),
            headers=headers,
            retries=False
        )

        logger.info(f'Response status: {response.status}')
        logger.info(f'Response data: {response.data}')

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Discord!')
    }
