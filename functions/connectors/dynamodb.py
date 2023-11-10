from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import List

from models.dynamodb import VideoStatistics
from models.dynamodb import VideoTimestamp


def store_statistics(table, statistics: VideoStatistics) -> None:
    response = table.put_item(Item=statistics.model_dump())


def get_video_list(table) -> List[VideoTimestamp]:
    # get all items that have an enddate gte today
    response = table.query(
        IndexName='entity-type-identifier',
        KeyConditionExpression=Key('entity_type').eq("Timestamp"),
        FilterExpression=Key('end_date').gte(datetime.now().strftime("%Y-%m-%d"))
    )

    return [VideoTimestamp(**resp) for resp in response['Items']]