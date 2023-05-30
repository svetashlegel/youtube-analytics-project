import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео с ютуб"""

    def __init__(self, video_id: str) -> None:
        """Инициализация видео по id, остальные данные получаются по API"""
        self.__video_id = video_id
        self.video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.__video_id).execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает название канала"""
        return f'{self.video_title}'


class PLVideo (Video):
    """Класс для видео и плейлиста с ютуб"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.__playlist_id = playlist_id
