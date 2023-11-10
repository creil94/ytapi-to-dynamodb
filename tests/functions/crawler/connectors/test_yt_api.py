import pytest
from unittest.mock import patch

from functions.crawler.connectors.yt_api import crawl_video_statistics, VideoNotFoundException


class MockResponse:
    '''Helper class to return a response object which has all the required functionalities'''
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


@pytest.fixture
def requests_client():
    def mock_api_call(data, **kwargs):
        # function that mocks response based on the video id
        if kwargs['params']['id'] == 'good_video':
            # normal video with normal stats
            stats = [{
                'statistics': {
                    'commentCount': '1',
                    'favoriteCount': '2',
                    'likeCount': '3',
                    'viewCount': '4'
                }
            }]
            response = {
                'items': stats
            }
            return MockResponse(response, 200)
        elif kwargs['params']['id'] == 'bad_video':
            # video that does not exist
            response = {
                'items': []
            }
            return MockResponse(response, 200)

    with patch('requests.get', new=mock_api_call):
        yield None


def test_crawl_video_statistics_good_video(requests_client):
    # test case for a normal video with normal stats
    video_stats = crawl_video_statistics('good_video')

    assert video_stats.comment_count == 1
    assert video_stats.favorite_count == 2
    assert video_stats.like_count == 3
    assert video_stats.view_count == 4


def test_crawl_video_statistics_bad_video(requests_client):
    # test a non existend video
    with pytest.raises(VideoNotFoundException):
        crawl_video_statistics('bad_video')