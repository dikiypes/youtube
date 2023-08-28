import os
import datetime
from googleapiclient.discovery import build
import isodate

class PlayList:
    def __init__(self, playlist_id):
        # api_key = os.getenv('ApiKey')
        api_key: str = 'AIzaSyAlkREa53g8ujIlII3doGa_lxEKzS3EMEM'
        self.youtube = build('youtube', 'v3', developerKey=api_key)

        playlist = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()
        playlist_snippet = playlist["items"][0]["snippet"]

        self.title = playlist_snippet["title"]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.playlist_id = playlist_id

    def total_duration(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        self.total_second = 0
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.total_second += duration.total_seconds()
        total_datetime = datetime.timedelta(seconds=self.total_second)
        return total_datetime

    def total_second(self):
        return self.total_second()

    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            max_like = 0
            best_url = ''
            url = f"https://youtu.be/{video['id']}"
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                max_like = like_count
                best_url = url
        return best_url

