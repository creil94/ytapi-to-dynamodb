import pytest
from unittest.mock import patch


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
        # if the video id contains something with 'bad_video' an empty response will be returned
        if 'bad_video' in kwargs['params']['id']:
            # video that does not exist
            response = {
                'items': []
            }
            return MockResponse(response, 200)

        # normal video with normal stats
        stats = [{
            'id': kwargs['params']['id'],
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

    with patch('requests.get', new=mock_api_call):
        yield None
