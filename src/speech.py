import os
from dotenv import load_dotenv
from TTS.api import TTS
import uberduck
import whisper
import requests

from src.capturing import Capturing


load_dotenv()


def transcribe_audio(filename: str):
    with Capturing() as output:
        transcriber = whisper.load_model("medium")
        result = transcriber.transcribe(filename)
        return result["text"]


def generate_audio_tts(answer: str, filepath: str):
    with Capturing() as output:
        tts = TTS(TTS.list_models()[0])
        tts.tts_to_file(
            text=answer,
            speaker=tts.speakers[1],
            language=tts.languages[0],
            file_path=filepath,
        )


def generate_audio_uberduck(answer: str, voice: str, filepath: str):
    with Capturing() as output:
        client = uberduck.UberDuck(
            os.getenv("UBERDUCK_API_KEY"), os.getenv("UBERDUCK_API_SECRET")
        )
        audio = client.speak(answer, voice=voice, play_sound=False)
        with open(filepath, mode="bw") as wav_file:
            wav_file.write(audio)
        return audio
    


def generate_audio_elevenlabs(answer: str, voice: str, filepath: str):
    with Capturing() as output:
        audio = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}', 
            data={
                "text": answer,
                "voice_settings": {
                "stability": 0,
                "similarity_boost": 0
            }},
            headers={
                'x-api-key': os.getenv("ELEVENLABS_API_KEY")
            }
        )
        
        with open(filepath, mode="bw") as file:
            file.write(audio)
        return audio
