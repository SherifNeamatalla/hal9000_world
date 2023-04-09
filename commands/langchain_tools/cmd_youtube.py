import json
import os

import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from langchain.agents import tool
from youtube_transcript_api import YouTubeTranscriptApi

from config.constants import YOUTUBE_AGENT_PRESET_NAME

load_dotenv()

API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')


@tool("YouTube Video Data")
def get_video_data(url):
    """Get the data of a YouTube video."""
    video_id = url.split('=')[1]
    endpoint = f'{API_BASE_URL}/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}'
    response = requests.get(endpoint)
    data = json.loads(response.content.decode('utf-8'))

    if len(data['items']) == 0:
        return 'No video found with that ID'

    video_data = {}
    video_data['title'] = data['items'][0]['snippet']['title']
    video_data['description'] = data['items'][0]['snippet']['description']
    video_data['channel'] = data['items'][0]['snippet']['channelTitle']
    return video_data


@tool("YouTube Video Captions")
def get_video_script(url):
    """Get the captions of a YouTube video."""
    from agents.config import AgentConfig
    video_id = url.split('v=')[1]

    browser_agent = AgentConfig.from_preset(YOUTUBE_AGENT_PRESET_NAME)

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # extract the text from the transcript

    transcript = '\n'.join([item['text'] for item in transcript])

    messages = [create_message(transcript)]

    return browser_agent.chat(messages)


def get_credentials():
    return service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])


def create_message(question):
    return {
        "role": "user",
        "content": f"Summarize the following youtube video transcript.\n\nTranscript:\n{question}"
    }


youtube_tools = [
    get_video_data,
    get_video_script,
]
