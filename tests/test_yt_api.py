import pytest

from functions.connectors.yt_api import crawl_video_statistics, VideoNotFoundException


def test_crawl_video_statistics_good_video(requests_client):
    # test case for a normal video with normal stats
    video_id = 'good_video_'
    video_stats = crawl_video_statistics(video_id)

    assert video_stats.video_id == video_id
    assert video_stats.comment_count == 1
    assert video_stats.favorite_count == 2
    assert video_stats.like_count == 3
    assert video_stats.view_count == 4
    assert video_stats.entity_type == 'Statistic'
    assert video_stats.identifier.startswith('STATS#')


def test_crawl_video_statistics_bad_video(requests_client):
    # test a non existent video
    with pytest.raises(VideoNotFoundException):
        crawl_video_statistics('bad_video__')