import os
import requests
from models.video_statistics import VideoStatistics


BASE_URL = "https://www.googleapis.com/youtube/v3/"
API_KEY = os.environ['YT_API_KEY']


def request(api_path: str, params: dict) -> dict:
    """
    function that takes care of requesting the yt api including pagination
    Args:
        api_path: path which shall be requested
        params: parameters which are sent to the path
    """
    # build path and add api key to params
    url = BASE_URL + api_path
    params['key'] = API_KEY

    # make initial request and yield the items
    response = requests.get(url, params=params)
    response.raise_for_status()
    for item in response.json()['items']:
        yield item

    # if there are multiple pages -> iterate over them and yield items
    while "nextPageToken" in response:
        params["pageToken"] = response["nextPageToken"]
        response = requests.get(url, params=params).json()
        for item in response['items']:
            yield item


def crawl_video_statistics(video_id: str) -> VideoStatistics:
    """
    function that crawls the latest statistics of the given video id
    Args:
        video_id: video_id for which the statistics shall be crawled

    Returns:
        statistics as dictionary
    """
    # prepare params for request
    params = {
        'part': 'statistics',
        'id': video_id
    }

    # iterate over the response from the api
    for item in request("videos", params):
        return VideoStatistics(**item['statistics'])
