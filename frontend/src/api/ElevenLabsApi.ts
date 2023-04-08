// voiceApi.ts

import axios, { AxiosResponse } from 'axios';

const API_KEY = process.env.REACT_APP_ELEVENLABS_API_KEY;

interface VoiceApiResponse {
  audioUrl: string;
}

export async function synthesizeSpeech(text: string, voice: string): Promise<string> {
  const requestBody = {
    text,
    voice,
  };

  try {
    const response: AxiosResponse<VoiceApiResponse> = await axios.post(
      `https://api.elevenlabs.io/v1/text-to-speech/${voice}`,
      requestBody,
      {
        headers: {
          'xi-api-key': `${API_KEY}`,
          'Content-Type': 'application/json',
        },
      },
    );

    // @ts-ignore
    return URL.createObjectURL(response.data);

    return response.data.audioUrl;
  } catch (error) {
    console.error('Error synthesizing speech:', error);
    throw error;
  }
}
