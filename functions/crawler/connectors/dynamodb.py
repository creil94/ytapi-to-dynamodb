from models.video_statistics import VideoStatistics


def store_statistics(table, statistics: VideoStatistics):
    response = table.put_item(Item=statistics.model_dump())