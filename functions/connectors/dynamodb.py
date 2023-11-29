from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import List
from aws_lambda_powertools import Tracer

from models.dynamodb import VideoStatistics
from models.dynamodb import VideoTimestamp


tracer = Tracer()


@tracer.capture_method
def store_statistics(table, statistics: VideoStatistics) -> None:
    tracer.put_annotation(key="video_id", value=statistics.video_id)
    response = table.put_item(Item=statistics.model_dump())


@tracer.capture_method
def get_video_list(table) -> List[VideoTimestamp]:
    # get all items that have an enddate gte today
    response = table.query(
        IndexName='entity-type-identifier',
        KeyConditionExpression=Key('entity_type').eq("Timestamp"),
        FilterExpression=Key('end_date').gte(datetime.now().strftime("%Y-%m-%d"))
    )

    return [VideoTimestamp(**resp) for resp in response['Items']]