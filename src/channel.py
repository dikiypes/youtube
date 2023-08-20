import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:

        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('ApiKey')

        # создать специальный объект для работы с API
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        channel_snippet = channel["items"][0]["snippet"]
        channel_statistics = channel["items"][0]["statistics"]

        self.channel_id = channel_id
        self.title = channel_snippet["title"]
        self.description = channel_snippet["description"]
        self.url = channel_snippet["customUrl"]
        self.subscriberCount = channel_statistics["subscriberCount"]
        self.video_count = channel_statistics["videoCount"]
        self.viewCount = channel_statistics["viewCount"]

    def get_service(self):
        return self.youtube

    def to_json(self, filename):
        bookjson = {"channel_id": self.channel_id,
                  "title": self.title,
                  "description": self.description,
                  "customUrl": self.url,
                  "subscriberCount": self.subscriberCount,
                  "video_count": self.video_count,
                  "viewCount": self.viewCount}

        print(bookjson["channel_id"])

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(bookjson, file, ensure_ascii=False)