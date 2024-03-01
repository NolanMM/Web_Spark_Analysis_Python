from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import re
import requests

from services.DataCollector import YouTubeDataCollector

url_sample = "https://www.youtube.com/"


class PysparkModule:
    chanel_id = ""
    channel_name = ""
    number_of_videos = 0

    def __init__(self, channel_name):
        # self.spark = SparkSession.builder.appName("PysparkModule").getOrCreate()
        self.channel_name = channel_name

    def get_channel_id(self):
        url_request = url_sample + self.channel_name
        response = requests.get(url_request)
        if response.status_code == 200:
            data = response.text
            match = re.search(r'"key":"browse_id","value":"([^"]+)"', data)
            if match:
                value = match.group(1)
                self.chanel_id = value
            else:
                self.chanel_id = None
        return self.chanel_id

    def collect_data(self):
        youtube_collector = YouTubeDataCollector(self.chanel_id)
        channel_stats = youtube_collector.get_channel_stats()
        playlist_id = youtube_collector.get_playlist_id(channel_stats)
        video_list = youtube_collector.get_video_list(playlist_id)
        number_of_videos = len(video_list)
        self.number_of_videos = number_of_videos
        video_data = youtube_collector.get_video_details(video_list)
        return self.number_of_videos, video_data

    # def stop(self):
    #     self.spark.stop()


# if __name__ == "__main__":
#     pyspark_module = PysparkModule("@Optimus96")
#     channel_id = pyspark_module.get_channel_id()
#     number_of_videos, video_data = pyspark_module.collect_data()
#     print(number_of_videos)
#     print(video_data[0])
#     pyspark_module.stop()
