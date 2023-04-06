import json
import os

import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from commands.cmd_interface import ICmd

load_dotenv()


class CmdYoutube(ICmd):
    API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
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
        endpoint = f'{self.API_BASE_URL}/videos?part=snippet&id={video_id}&key={self.YOUTUBE_API_KEY}'
        response = requests.get(endpoint)
        data = json.loads(response.content.decode('utf-8'))

        if len(data['items']) == 0:
            return 'No video found with that ID'

        video_data = {}
        video_data['title'] = data['items'][0]['snippet']['title']
        video_data['description'] = data['items'][0]['snippet']['description']
        video_data['channel'] = data['items'][0]['snippet']['channelTitle']
        return video_data

    # def get_video_script(self, url):
    #     # Extract the video ID from the URL
    #     video_id = url.split('v=')[1]
    #
    #     if not video_id:
    #         return 'Invalid YouTube video URL.'
    #
    #     # Authenticate with the YouTube Data API
    #
    #     credentials = self.get_credentials()
    #     # if not credentials or not credentials.valid:
    #     #     if credentials and credentials.expired and credentials.refresh_token:
    #     #         credentials.refresh(Request())
    #     #     else:
    #     #         return 'Unable to authenticate with the YouTube Data API.'
    #
    #     youtube = build('youtube', 'v3', credentials=credentials)
    #
    #     # Retrieve the captions for the video
    #     caption_request = youtube.captions().list(
    #         part='snippet',
    #         videoId=video_id
    #     )
    #
    #     caption_response = caption_request.execute()
    #
    #     # Get the first caption track
    #     if not caption_response.get('items'):
    #         return 'No captions available for this video.'
    #
    #     caption_track = caption_response['items'][0]
    #     caption_id = caption_track['id']
    #
    #     # Download the caption
    #     caption_download_request = youtube.captions().download(
    #         id=caption_id
    #     )
    #
    #     caption_download_response = caption_download_request.execute()
    #     caption_content = caption_download_response.decode('utf-8')
    #
    #     return caption_content

    def get_video_script(self, url):
        from agents.browser_agent import BrowserAgent
        video_id = url.split('v=')[1]

        browser_agent = BrowserAgent()

        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # extract the text from the transcript

        transcript = '\n'.join([item['text'] for item in transcript])

        messages = [self.create_message(transcript)]

        return browser_agent.chat(messages)

    def get_credentials(self):
        return service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

    def create_message(self, question):
        return {
            "role": "user",
            "content": f"Summarize the following youtube video transcript.\n\nTranscript:\n{question}"
        }
