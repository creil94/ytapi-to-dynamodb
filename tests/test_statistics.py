import json

from functions.crawler.statistics import lambda_handler


def test_statistics_inserting_stats_one_video(video_table_mock, requests_client):
    '''tests the results of what happens when statistics for one video are retrieved
    expected result: table has one record with exactly the details of the video'''
    video_id = 'good_video_'
    lambda_handler({'Records': [{'body': json.dumps({'VideoId': video_id})}]}, None)

    # check if video stats are in table
    results = video_table_mock.scan(TableName='Videos')

    assert 'Items' in results
    assert len(results['Items']) == 1
    assert results['Items'][0]['video_id']['S'] == video_id


def test_statistics_inserting_stats_multiple_videos(video_table_mock, requests_client):
    '''tests the results of what happens when statistics for multiple videos are retrieved
    expected result: table has multiple record with exactly the details of the videos'''
    records = [
        {
            'body': json.dumps({'VideoId': 'good_video1'})
        },
        {
            'body': json.dumps({'VideoId': 'good_video2'})
        },
        {
            'body': json.dumps({'VideoId': 'good_video3'})
        },
    ]

    lambda_handler({'Records': records}, None)

    # check if video stats are in table
    results = video_table_mock.scan(TableName='Videos')

    assert 'Items' in results
    assert len(results['Items']) == 3

    assert results['Items'][0]['video_id']['S'] == 'good_video1'
    assert 'comment_count' in results['Items'][0]
    assert 'favorite_count' in results['Items'][0]
    assert 'like_count' in results['Items'][0]
    assert 'view_count' in results['Items'][0]
    assert results['Items'][0]['entity_type']['S'] == 'Statistic'
    assert results['Items'][0]['identifier']['S'].startswith('STATS#')

    assert results['Items'][1]['video_id']['S'] == 'good_video2'
    assert 'comment_count' in results['Items'][1]
    assert 'favorite_count' in results['Items'][1]
    assert 'like_count' in results['Items'][1]
    assert 'view_count' in results['Items'][1]
    assert results['Items'][1]['entity_type']['S'] == 'Statistic'
    assert results['Items'][1]['identifier']['S'].startswith('STATS#')

    assert results['Items'][2]['video_id']['S'] == 'good_video3'
    assert 'comment_count' in results['Items'][2]
    assert 'favorite_count' in results['Items'][2]
    assert 'like_count' in results['Items'][2]
    assert 'view_count' in results['Items'][2]
    assert results['Items'][2]['entity_type']['S'] == 'Statistic'
    assert results['Items'][2]['identifier']['S'].startswith('STATS#')


def test_statistics_inserting_stats_bad_video(video_table_mock, requests_client):
    '''tests the results of what happens when statistics for video are retrieved, that does not exist
    expected result: lambda throws exception and table remains empty'''
    video_id = 'bad_video__'

    try:
        lambda_handler({'Records': [{'body': json.dumps({'VideoId': video_id})}]}, None)
    except:
        pass

    # check if video stats are in table
    results = video_table_mock.scan(TableName='Videos')

    assert 'Items' in results
    assert len(results['Items']) == 0