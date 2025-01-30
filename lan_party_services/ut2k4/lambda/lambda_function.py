import os
import json
import urllib3
import logging
import base64
import gzip
from io import BytesIO

http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    webhook_url = "https://canary.discord.com/api/webhooks/1334127928706994248/8tCtJ17nmOxP6bI-dVhH3C0Hh71xSydbGr-94H8Igm959rPHjew6ilYMJ4qplXP3RLp_"
    # webhook_url = os.environ['WEBHOOK_URL']
    logger.info(f"Log event: {event}")

    if "awslogs" not in event:
        logger.error("No awslogs found in event")
        return {"statusCode": 400, "body": json.dumps("No awslogs found in event")}

    # Decode the base64-encoded and gzip-compressed log data
    compressed_payload = base64.b64decode(event["awslogs"]["data"])
    with gzip.GzipFile(fileobj=BytesIO(compressed_payload)) as gzipfile:
        log_data = json.loads(gzipfile.read().decode("utf-8"))

    # Extract log events
    for log_event in log_data["logEvents"]:
        message = log_event["message"]
        logger.info(f"Log message: {message}")

        # Prepare the message payload
        msg = {"username": "UT2k4 Server Bot", "content": f"{message}"}
        logger.info(f"Log msg: {msg}")
        headers = {"Content-Type": "application/json"}

        # Send the message to the Discord webhook
        response = http.request(
            "POST", webhook_url, body=json.dumps(msg), headers=headers, retries=False
        )

        logger.info(f"Response status: {response.status}")
        logger.info(f"Response data: {response.data}")

    return {"statusCode": 200, "body": json.dumps("Message sent to Discord!")}
