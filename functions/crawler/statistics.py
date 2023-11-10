import os
import json
import boto3

from connectors.yt_api import crawl_video_statistics
from connectors.dynamodb import store_statistics
from models.video_event import VideoEvent

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VIDEO_TABLE'])


def lambda_handler(event, context):
    # check if event has correct format
    if 'Records' not in event or type(event['Records']) != list:
        raise ValueError('Not a valid event')

    # iterate over every record, iterate video id, request statistics and store in dynamodb
    for record in event['Records']:
        video_event = VideoEvent(**json.loads(record['body']))
        statistics = crawl_video_statistics(video_event.video_id)

        store_statistics(table, statistics)
