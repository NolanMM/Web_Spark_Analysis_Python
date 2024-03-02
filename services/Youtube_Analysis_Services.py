from datetime import datetime, timedelta

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
        transformed_data = self.transform_data(video_data)
        return transformed_data

    def transform_data(self, video_data):
        table_data = []
        total_views = 0
        total_likes = 0
        total_dislikes = 0
        total_engagement = 0

        for idx, video in enumerate(video_data, start=1):
            video_id = str(idx)
            video_title = video['title']
            view_count = video['views_count']
            like_count = video['likes_count']
            dislikes_count = video['dislikes_count']
            comments_count = video['comments_count']
            additional_info = "Additional Info " + video_id

            # Convert view_count, like_count, dislikes_count, comments_count to int
            view_count = int(view_count)
            like_count = int(like_count)
            dislikes_count = int(dislikes_count)
            comments_count = int(comments_count)
            total_views += view_count
            total_likes += like_count
            total_dislikes += dislikes_count
            total_engagement += comments_count

            video_entry = {
                "VideoID": video_id,
                "VideoTitle": video_title,
                "ViewCount": view_count,
                "LikeCount": like_count,
                "DislikesCount": dislikes_count,
                "CommentsCount": comments_count,
                "AdditionalInformation": additional_info
            }

            table_data.append(video_entry)

        monthly_data = self.get_monthly_data(video_data)

        data = {
            'table_data': table_data,
            'TotalViews': total_views,
            'TotalLikes': total_likes,
            'TotalDislikes': total_dislikes,
            'TotalEngagement': total_engagement,
            'labels': monthly_data['labels'],
            'views': monthly_data['views'],
            'likes': monthly_data['likes'],
            'dislikes': monthly_data['dislikes'],
            'engagement': monthly_data['engagement']
        }

        return data

    def get_monthly_data(self,video_data):
        monthly_data = {month: {'views': 0, 'likes': 0, 'dislikes': 0, 'engagement': 0} for month in range(1, 13)}

        one_year_ago = datetime.now() - timedelta(days=365)

        for video in video_data:
            published_date = datetime.strptime(video['published'], "%Y-%m-%dT%H:%M:%SZ")
            if published_date >= one_year_ago:
                month = published_date.month
                # Convert view_count, like_count, dislikes_count, comments_count to int
                view_count = int(video['views_count'])
                likes_count = int(video['likes_count'])
                dislikes_count = int(video['dislikes_count'])
                comments_count = int(video['comments_count'])
                monthly_data[month]['views'] += view_count
                monthly_data[month]['likes'] += likes_count
                monthly_data[month]['dislikes'] += dislikes_count
                monthly_data[month]['engagement'] += comments_count

        labels = []
        views = []
        likes = []
        dislikes = []
        engagement = []

        for month in range(1, 13):
            labels.append(datetime.now().replace(month=month).strftime('%B'))
            views.append(monthly_data[month]['views'])
            likes.append(monthly_data[month]['likes'])
            dislikes.append(monthly_data[month]['dislikes'])
            engagement.append(monthly_data[month]['engagement'])

        return {
            'labels': labels,
            'views': views,
            'likes': likes,
            'dislikes': dislikes,
            'engagement': engagement
        }
    # def stop(self):
    #     self.spark.stop()


# if __name__ == "__main__":
#     pyspark_module = PysparkModule("@Optimus96")
#     channel_id = pyspark_module.get_channel_id()
#     transformed_data = pyspark_module.collect_data()
#     print(transformed_data)
#     pyspark_module.stop()
