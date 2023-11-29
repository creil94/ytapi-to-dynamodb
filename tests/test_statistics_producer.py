import os
import json
from typing import List

import pytest

from functions.producer.statistics import lambda_handler


def insert_record_helper(dynamo_client, items: List):
    '''Helper that inserts the given items in "items" to the respective table'''
    for item in items:
        response = dynamo_client.put_item(
            TableName=os.environ['VIDEO_TABLE'],
            Item=item
        )


@pytest.fixture
def single_record(video_table_mock):
    # insert test record into table
    items = [
        {
            'video_id': {'S': 'good_video_'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2099-01-01'}
        }
    ]

    insert_record_helper(video_table_mock, items)


@pytest.fixture
def single_record_outdated(video_table_mock):
    # insert test record into table
    items = [
        {
            'video_id': {'S': 'good_video_'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2010-01-01'}
        }
    ]

    insert_record_helper(video_table_mock, items)


@pytest.fixture
def multi_records(video_table_mock):
    # insert multiple test records into table
    items = [
        {
            'video_id': {'S': 'good_video1'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2099-01-01'}
        },
        {
            'video_id': {'S': 'good_video2'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2099-01-01'}
        }
    ]

    insert_record_helper(video_table_mock, items)


@pytest.fixture
def multi_records_mixed(video_table_mock):
    # insert multiple test records into table
    items = [
        {
            'video_id': {'S': 'good_video1'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2010-01-01'}
        },
        {
            'video_id': {'S': 'good_video2'},
            'identifier': {'S': 'TIMESTAMP'},
            'entity_type': {'S': 'Timestamp'},
            'end_date': {'S': '2099-01-01'}
        }
    ]

    insert_record_helper(video_table_mock, items)


def test_producer_e2e_single_video(video_table_mock, video_sqs_mock, single_record, lambda_context):
    '''Tests if a single video makes it to the queue'''
    lambda_handler(None, lambda_context)

    # check if message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' in message
    assert len(message['Messages']) == 1
    assert json.loads(message['Messages'][0]['Body'])['video_id'] == 'good_video_'

    # check if queue is empty
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])
    assert 'Messages' not in message


def test_producer_e2e_multiple_videos(video_table_mock, video_sqs_mock, multi_records, lambda_context):
    '''Tests if multiple videos makes it to the queue'''
    lambda_handler(None, lambda_context)

    # check if first message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' in message
    assert len(message['Messages']) == 1
    assert json.loads(message['Messages'][0]['Body'])['video_id'] == 'good_video1'

    # check if second message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' in message
    assert len(message['Messages']) == 1
    assert json.loads(message['Messages'][0]['Body'])['video_id'] == 'good_video2'

    # check if queue is empty
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])
    assert 'Messages' not in message


def test_producer_e2e_no_videos(video_table_mock, video_sqs_mock, lambda_context):
    '''tests what happens if no video were in the table. Expected behaviour is that the queue is empty'''
    lambda_handler(None, lambda_context)

    # check if first message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' not in message


def test_producer_e2e_outdated_videos(video_table_mock, video_sqs_mock, single_record_outdated, lambda_context):
    '''tests what happens if only and outdated video is in the table. Expected behaviour is that the queue is empty'''
    lambda_handler(None, lambda_context)

    # check if first message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' not in message


def test_producer_e2e_single_and_outdated_videos(video_table_mock, video_sqs_mock, multi_records_mixed, lambda_context):
    '''tests what happens if a non outdated and an outdated video are in the table.
    Expected behaviour is that only the non outdated made it to the queue'''
    lambda_handler(None, lambda_context)

    # check if message arrived on the queue
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])

    assert 'Messages' in message
    assert len(message['Messages']) == 1
    assert json.loads(message['Messages'][0]['Body'])['video_id'] == 'good_video2'

    # check if queue is empty
    message = video_sqs_mock.receive_message(QueueUrl=os.environ['QUEUE_URL'])
    assert 'Messages' not in message
