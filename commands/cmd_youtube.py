import json
import os

import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

from commands.cmd_interface import ICmd

load_dotenv()


class CmdYoutube(ICmd):
    API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

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

        if not video_id:
            return 'Invalid YouTube video URL.'

        # Authenticate with the YouTube Data API

        credentials = self.get_credentials()
        # if not credentials or not credentials.valid:
        #     if credentials and credentials.expired and credentials.refresh_token:
        #         credentials.refresh(Request())
        #     else:
        #         return 'Unable to authenticate with the YouTube Data API.'

        youtube = build('youtube', 'v3', credentials=credentials)

        # Retrieve the captions for the video
        caption_request = youtube.captions().list(
            part='snippet',
            videoId=video_id
        )

        caption_response = caption_request.execute()

        # Extract the transcript from the caption track
        transcript_url = caption_response['items'][0]['snippet']['trackUrl']
        transcript_request = requests.get(transcript_url)
        transcript_lines = transcript_request.text.strip().split('\n')[1:]

        transcript = ''
        for line in transcript_lines:
            if line.strip():
                transcript += line.strip() + ' '

        return transcript.strip()

    def get_credentials(self, ):
        return service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/cloud-platform'])
