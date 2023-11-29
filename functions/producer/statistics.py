import os
import boto3
from aws_lambda_powertools import Tracer

from connectors.dynamodb import get_video_list
from connectors.sqs import send_message


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VIDEO_TABLE'])
sqs_client = boto3.client("sqs")
tracer = Tracer()
QUEUE_URL = os.environ['QUEUE_URL']


@tracer.capture_lambda_handler
def lambda_handler(event, context):
    # get list of videos
    video_list = get_video_list(table)

    # add them to the queue
    for video in video_list:
        send_message(sqs_client, QUEUE_URL, video.model_dump(exclude={'end_date'}))