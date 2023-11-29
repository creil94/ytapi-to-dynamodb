import os
import json
import boto3
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord

from connectors.yt_api import crawl_video_statistics
from connectors.dynamodb import store_statistics
from models.video_event import VideoEvent

VIDEO_TABLE = os.environ['VIDEO_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(VIDEO_TABLE)
tracer = Tracer()
logger = Logger(log_uncaught_exceptions=True)
processor = BatchProcessor(event_type=EventType.SQS)


@tracer.capture_method
def record_handler(record: SQSRecord):
    # request statistics and store in dynamodb
    video_event = VideoEvent(**json.loads(record['body']))
    statistics = crawl_video_statistics(video_event.video_id)

    store_statistics(table, statistics)


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    # check if event has correct format
    if 'Records' not in event or type(event['Records']) != list:
        raise ValueError('Not a valid event')

    return process_partial_response(
        event=event,
        record_handler=record_handler,
        processor=processor,
        context=context,
    )
