import json
import os

import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.errors
import requests
from dotenv import load_dotenv

from commands.cmd_interface import ICmd

load_dotenv()


class CmdYoutube(ICmd):
    API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
    API_KEY = os.getenv('YOUTUBE_API_KEY')

    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type=None):
        if cmd_type == 'get_video_data':
            return self.get_video_data(cmd_args['url'])
        elif cmd_type == 'get_video_script':
            return self.get_video_script(cmd_args['url'])
        else:
            return 'Invalid command type'

    def get_video_data(self, url):
        video_id = url.split('=')[1]
        endpoint = f'{self.API_BASE_URL}/videos?part=snippet&id={video_id}&key={self.API_KEY}'
        response = requests.get(endpoint)
        data = json.loads(response.content.decode('utf-8'))

        if len(data['items']) == 0:
            return 'No video found with that ID'

        video_data = {}
        video_data['title'] = data['items'][0]['snippet']['title']
        video_data['description'] = data['items'][0]['snippet']['description']
        video_data['channel'] = data['items'][0]['snippet']['channelTitle']
        return video_data

    def get_video_script(self, url):
        # Extract the video ID from the URL
        video_id = url.split('v=')[1]

        flow = google.auth.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file,
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
        )
        credentials = flow.run_local_server()
        # Create a YouTube API client
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.API_KEY)

        # Retrieve the video caption tracks
        caption_tracks = youtube.captions().list(
            part='id',
            videoId=video_id
        ).execute()

        # Retrieve the captions for each track
        captions = []
        for track in caption_tracks['items']:
            caption = youtube.captions().download(
                id=track['id'],
                tfmt='vtt'
            ).execute()
            captions.append(caption)

        # Return the captions as a list of VTT files
        return captions
