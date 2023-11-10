import json

from connectors.yt_api import crawl_video_statistics
from models.video_event import VideoEvent


def lambda_handler(event, context):
    if 'Records' not in event or type(event['Records']) != list:
        raise ValueError('Not a valid event')

    for record in event['Records']:
        video_event = VideoEvent(**json.loads(record['body']))
        statistics = crawl_video_statistics(video_event.video_id)

        print(statistics)
