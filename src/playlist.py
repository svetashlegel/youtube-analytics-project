import os
import isodate
from googleapiclient.discovery import build
from datetime import timedelta

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """Класс для плейлиста с ютуб"""

    def __init__(self, playlist_id: str) -> None:
        """Инициализация видео по id, остальные данные получаются по API"""

        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=playlist_id,
                                                 part='snippet, contentDetails', maxResults=50, ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        """Возвращает суммарную продолжительность видео плейлиста"""
        total_duration = timedelta(0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео по кол-ву лайков"""
        max_likes = 0
        best_video = ''
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                best_video = video
        return f"https://youtu.be/{best_video['id']}"
