import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        # api_key = os.getenv('ApiKey')
        api_key: str = 'AIzaSyAlkREa53g8ujIlII3doGa_lxEKzS3EMEM'
        youtube = build('youtube', 'v3', developerKey=api_key)

        video = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        video_snippet = video["items"][0]["snippet"]
        video_statistics = video["items"][0]["statistics"]

        self.id = video_id
        self.title = video_snippet["title"]
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.viewCount = video_statistics["viewCount"]
        self.likeCount = video_statistics["likeCount"]

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


