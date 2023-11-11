import os
import pytest
import boto3
from moto import mock_dynamodb


@pytest.fixture
def video_table_mock():
    '''Mock for the video table'''
    with mock_dynamodb():
        client = boto3.client("dynamodb")
        client.create_table(
            TableName=os.environ['VIDEO_TABLE'],
            AttributeDefinitions=[
                {
                    'AttributeName': 'video_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'identifier',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'entity_type',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'video_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'identifier',
                    'KeyType': 'RANGE'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'entity-type-identifier',
                    'KeySchema': [
                        {
                            'AttributeName': 'entity_type',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'identifier',
                            'KeyType': 'RANGE'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
        )

        yield client