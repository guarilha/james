import openai
import os
import re
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_chatgpt(question: str):
    try:
        return openai.ChatCompletion.create(
        model="gpt-4", # 
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )
    except:
        print('deu ruim')
        return
    


def get_answer_text(answer, extract_code=True):
    t = answer.choices[0].message.content
    if extract_code:
        return extract_code_from_text(t)
    return t


def extract_code_from_text(text):
    code_pattern = re.compile(r'```[\s\S]*?```')
    code_list = []
    def replace_code(match):
        code_string = match.group()  # Modified function
        code_list.append((len(code_list) + 1, code_string))
        return f"[see code snippet #{len(code_list)}]"
    output_text = re.sub(code_pattern, replace_code, text)
    return output_text, sorted(code_list, key=lambda x: x[0])
