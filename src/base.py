
from src.prompts import do_command, filter_news, short_message, summarize
from src.web import get_text_from_url, get_top_from_cnn, get_top_from_hackernews

from src.audio import play_audio, record_audio
from src.speech import generate_audio_elevenlabs, transcribe_audio, generate_audio_tts, generate_audio_uberduck
from src.openai import ask_chatgpt, get_answer_text

import json

def api_ask(question: str, character: str = "an AI Assistant", play: str=False, content: str=None, voice: str=None):
    
    # question = transcribe_audio(filename)
    
    if content:
        question = question + f"\n\n```\n{content}\n```\n"

    answer = ask_chatgpt(short_message(question, character))
    
    full_text_answer = get_answer_text(answer, extract_code=False)
    text_answer, code = get_answer_text(answer)
    
    audio = None
    if play:
        if play == 'tts':    
            audio = "output/tts_answer.wav"
            audio_file = generate_audio_tts(text_answer, audio)
        elif play == 'uberduck':
            audio = "output/uberduck_answer.wav"
            audio_file = generate_audio_uberduck(text_answer, voice, audio)
        elif play == 'elevenlabs':
            audio = "output/tts_answer.wav"
            audio_file = generate_audio_elevenlabs(text_answer, voice, audio)

    a = answer.to_dict_recursive()

    with open('output/lastAnswer.json', 'w') as file:
        file.write(json.dumps(a))

    return {
        "answer": a,
        "text": full_text_answer, 
        "audio": audio
    }, audio_file