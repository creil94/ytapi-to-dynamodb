import json


def send_message(sqs_client, queue_url, message):
    response = sqs_client.send_message(
        MessageBody=json.dumps(message),
        QueueUrl=queue_url
    )