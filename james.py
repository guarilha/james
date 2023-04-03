from dotenv import load_dotenv
import rich
import json
from src.prompts import do_command, filter_news, short_message, summarize
from src.web import get_text_from_url, get_top_from_cnn, get_top_from_hackernews

load_dotenv()
from rich.table import Table
import pyperclip  
import click 
from rich.markdown import Markdown
from rich.console import Console

from src.audio import play_audio, record_audio
from src.speech import generate_audio_elevenlabs, transcribe_audio, generate_audio_tts, generate_audio_uberduck
from src.openai import ask_chatgpt, get_answer_text

console = Console()

@click.group()
def cli():
    """Voice and text interaction with Chat GPT."""
    rich.print("\n:robot: [green]Hi, this is James reporting for duty. :brain:\n")
    # pass

@cli.command(name="ask")
@click.option(
    "--question",
    "-q",
    help="Bypass capturing the mic audio and speech to text",
)
@click.option(
    "--character",
    "-c",
    default="a Senior Software Engineer",
    help="A profession, a name of a famous person or from fiction (movies, series, etc)",
)
@click.option(
    "--play",
    "-p",
    type=click.STRING,
    help="Read outloud the answer at end. Options are: tts, uberduck, elevenlabs",
)
@click.option(
    "--file",
    "-f",
    type=click.File('r'),
    help="Upload a text or code file at the end of your prompt",
)
@click.option(
    "--save",
    "-s",
    type=click.File('w'),
    help="Save the answer on a file",
)
@click.option(
    "--no-clipboard",
    "-b",
    is_flag=True,
    help="Avoid copying code content to the clipboard",
)
@click.option(
    "--voice",
    "-v",
    type=click.STRING,
    help="Voice (index, name, ID) depending on the play option (tts, uberduck, elevenlabs)",
)
def ask(question: str, character: str, play: str, file: str, save: str, no_clipboard: bool,  voice: str):
    if not question:
        with console.status("[bold red]Recording...") as status:
            filename = record_audio(filename="question.wav")
        
        with console.status("[bold green]Transcribing audio...") as status:            
            question = transcribe_audio(filename)
    
    if file:
        with console.status("[bold green]Adding your file...") as status:            
            content  = file.read()
            question = question + f"\n\n```\n{content}\n```\n"

    with console.status("[bold green]Thinking...") as status:
        answer = ask_chatgpt(short_message(question, character))
    
    full_text_answer = get_answer_text(answer, extract_code=False)
    text_answer, code = get_answer_text(answer)

    rich.print("\n\n:question: [bold cyan]Question:")
    rich.print(Markdown(question))
    rich.print("\n\n:clipboard: [bold cyan]ANSWER:")
    rich.print(Markdown(full_text_answer))
    
    if play:
        if play == 'tts':
            with console.status("[bold green]Generate answer audio file...") as status:
                generate_audio_tts(text_answer, "output/tts_answer.wav")
        elif play == 'uberduck':
            with console.status("[bold green]Generate answer audio file...") as status:
                generate_audio_uberduck(text_answer, voice, "output/uberduck_answer.wav")
        elif play == 'elevenlabs':
            with console.status("[bold green]Generate answer audio file...") as status:
                generate_audio_elevenlabs(text_answer, voice, "output/tts_answer.wav")
        with console.status("[bold red]Playing answer...") as status:
            click.echo(click.style("Play Audio", fg='blue'))
            play_audio(f"output/{play}_answer.wav")
            click.echo()
    
    if not no_clipboard:
        copy = ""
        if code:
            for i,c in enumerate(code):
                copy += f"Code Snippet #{i+1}:\n{c[1]}\n\n"
        else:
            copy = full_text_answer
        pyperclip.copy(copy)

    if save: 
        with console.status("[bold green]Saving the answer...") as status:
            with open(save.name, 'w') as file:
                file.write(full_text_answer)
    
    rich.print("\n\n:thumbs_up: [green]Anything else? :thought_balloon:")
    

@cli.command(name="news")
@click.option(
    "--category",
    "-c",
    default='hackernews',
    type=click.STRING,
    help="Search from Hacker News or selected news sites (CNN, etc)",
)
@click.option(
    "--number",
    "-n",
    default=10,
    type=click.INT,
    help="",
)
@click.option(
    "--position",
    "-p",
    default=0,
    type=click.INT,
    help="",
)
@click.option(
    "--is-list",
    "-l",
    is_flag=True,
    help="Avoid news summaries and only print a list",
)
@click.option(
    "--save",
    "-s",
    type=click.File('w'),
    help="Save the answer on a file",
)
def news(category: str, number: int, position: int, is_list: bool, save: str):
    rich.print("\n:clipboard: [bold cyan]ANSWER:")
    if category == 'hackernews':
        if position:
            with console.status("[bold green]TLDR'ing news...") as status:
                news = get_top_from_hackernews(position)
                item = news[position - 1]
                if item.url: 
                    text = get_text_from_url(item.url)
                else: 
                    text = get_text_from_url(f"https://news.ycombinator.com/item?id={item.item_id}")
                
                answer = ask_chatgpt(summarize(text))
                if answer: 
                    s = Markdown(get_answer_text(answer, extract_code=False))
                else:
                    s = f"Sorry, your question was too long or we had a problem accessing the LLM. For this item: {item}"
            print_news_summary(item, s)
        else:
            items = get_top_from_hackernews(number)
            for item in items:
                with console.status("[bold green]TLDR'ing news...") as status:
                    if item.get('url'): 
                        text = get_text_from_url(item.get('url'))
                    else: 
                        text = get_text_from_url(f"https://news.ycombinator.com/item?id={item.item_id}")

                    answer = ask_chatgpt(summarize(text))
                    if answer:
                        s = Markdown(get_answer_text(answer, extract_code=False))
                    else:
                        s = f"Sorry, your question was too long or we had a problem accessing the LLM. For this item: {item}"
                print_news_summary(item, s)
        
        rich.print("\n\n:thumbs_up: [green]Anything else? :thought_balloon:")
    else:
        with console.status("[bold green]Filtering news...") as status:
            news = get_top_from_cnn()
            tech = get_top_from_hackernews(30)
            for t in tech: 
                news.append({
                    'title': t.get('title'),
                    'url': t.get('url'),
                })
            answer = ask_chatgpt(filter_news(news, filter=category))
            j = get_answer_text(answer, extract_code=False)
            try: 
                items = json.loads(j)
            except:
                rich.print(j)
                return 

        if(is_list): 
            md = f"# Top News on {category}\n\n"

            for item in items:
                md += f"1. [{item.get('title')}]({item.get('url')})\n"
            rich.print(Markdown(md))
            if save: 
                with console.status("[bold green]Saving the answer...") as status:
                    with open(save.name, 'w') as file:
                        file.write(md)
        else:
            for item in items:
                with console.status("[bold green]TLDR'ing news...") as status:
                    if item.get('url'): 
                        text = get_text_from_url(item.get('url'))
                        answer = ask_chatgpt(summarize(text))
                        s = Markdown(get_answer_text(answer, extract_code=False))
                        print_news_summary(item, s) 
            if save: 
                with console.status("[bold green]Saving the answer...") as status:
                    with open(save.name, 'w') as file:
                        file.write(json.dumps(items))


def print_news_summary(item, summary):    
    rich.print()
    rich.print(Markdown(f"# [{item.get('title')}]({item.get('url')})"))
    rich.print(summary)
    if item.get('item_id'):
        rich.print(Markdown(f"> [View on Hacker News](https://news.ycombinator.com/item?id={item.item_id})"))

    
    



@cli.command(name="tldr")
@click.option(
    "--url",
    "-u",
    type=click.STRING,
    help="A url to generate a summary of the text",
)
def tldr(url: str):
    rich.print("\n:clipboard: [bold cyan]ANSWER:")
    with console.status("[bold green]TLDR'ing URL...") as status:
        text = get_text_from_url(url)
        answer = ask_chatgpt(summarize(text))
        s = Markdown(get_answer_text(answer, extract_code=False))
        rich.print(s)
            
    rich.print("\n\n:thumbs_up: [green]Anything else? :thought_balloon:")
    
