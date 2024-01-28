import os
import pytest
import boto3
from moto import mock_aws


@pytest.fixture
def video_sqs_mock():
    '''Mock for the sqs queue'''
    with mock_aws():
        client = boto3.client("sqs")
        client.create_queue(
            QueueName=os.environ['VIDEO_QUEUE'],
        )

        yield client