import os

import gtts
import requests
from playsound import playsound

from config.env_loader import load_env
from voice.voice_manager_interface import IVoiceManager

load_env()
eleven_labs_voices = {
    "old_f_australian": "yb4LSSX00nWconeQQujS",
    "young_f_british": "5OBhy9rwDPoHd4oqEeDd"

}

tts_headers = {
    "Content-Type": "application/json",
    "xi-api-key": os.getenv('ELEVENLABS_API_KEY')
}


def eleven_labs_speech(text, voice_name='young_f_british'):
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
        voice_id=eleven_labs_voices[voice_name])
    formatted_message = {"text": text}
    response = requests.post(
        tts_url, headers=tts_headers, json=formatted_message)

    if response.status_code == 200:
        with open("speech.mpeg", "wb") as f:
            f.write(response.content)
        playsound("speech.mpeg")
        os.remove("speech.mpeg")
        return True
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
        return False


def gtts_speech(text):
    tts = gtts.gTTS(text)
    tts.save("speech.mp3")
    playsound("speech.mp3")
    os.remove("speech.mp3")


class ElevenLabsVoiceManager(IVoiceManager):
    def speak(self, text):
        if not os.getenv('ELEVENLABS_API_KEY'):
            gtts_speech(text)
        else:
            success = eleven_labs_speech(text)
            if not success:
                gtts_speech(text)
