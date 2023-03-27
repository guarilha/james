def short_message(question: str, character: str):
    return f"I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. Do not write any explanations. Only answer like {character}. You must know all of the knowledge of {character}. Always format your answers in Markdown. If your answer contains or is just code, always include it in a markdown-style code block.\n\Question: {question}\nAnswer:"

def do_command(question: str):
    return f"I want you to act as a command identifier. I will type text and you will reply with what command I want to run. My available commands are: 1. ls: list all files on the current dir\n2. cat: show the contents of a file\n. You only respond one of these commands with the appropriate args if any. My first text is: {question}"


def summarize(text: str):
    return f"I want you to condense a large text to bullet points with the important information. My first text is: \n{text}"


def filter_news(items, filter: str):
    prompt = f"I want you to filter news from the category {filter} from this list bellow. Don't skip any news, include all that remotely relates to the category {filter}. Format your answers in a JSON array of objects (with properties title and url) without comments or explanations. \n\n"
    
    for item in items:
        prompt += f"{item.get('title')}: {item.get('url')}\n"

    return prompt