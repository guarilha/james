import requests
from rich.table import Table
from bs4 import BeautifulSoup
from src.openai import ask_chatgpt, get_answer_text
from src.prompts import summarize
from rich.markdown import Markdown

from src.services.hackernews import HackerNewsApi

hn = HackerNewsApi()


def get_text_from_url(url):
    response = requests.get(f"{url}")
    if not response.ok:
        response = requests.get(f"https://webcache.googleusercontent.com/search?q=cache:{url}&strip=1&vwsrc=0")
    soup = BeautifulSoup(response.content, "html.parser")

    for tag in soup.find_all(True, {"class": ["comment", "comment-tree", "comments"]}):
         tag.decompose() 

    return soup.get_text()


def get_top_from_hackernews(limit=20):
    top = hn.top_stories(limit)
    items = []
    for id in top:
        item = hn.get_item(id)
        items.append(item)
    return items


# def print_items_from_hackernews(items):
#     table = Table()
#     table.add_column('id')
#     table.add_column('title')
#     table.add_column('url')
#     table.caption = "Hacker News Top Posts"
#     for item in items:
#         table.add_row(f"{item.item_id}" , item.title, item.url)
#     rich.print(table)


def get_top_from_cnn():
    response = requests.get("https://lite.cnn.com/")
    soup = BeautifulSoup(response.text, "html.parser")
    latest_stories = []


    for tag in soup.find_all(["nav", "header", "head", "footer", "aside", "script", "meta"]):
        tag.decompose()

    for article in soup.find_all("a"):
        if article.get("href") and article.get("href").startswith("/"):
            latest_stories.append({"title": article.text.strip(), "url": f"https://lite.cnn.com{article['href']}"})

    return latest_stories





# def get_text_from_url(url):
#     response = requests.get(f"https://12ft.io/proxy?q={url}")
#     soup = BeautifulSoup(response.content, "html.parser")

#     for tag in soup.find_all(["nav", "header", "footer", "aside", "script", "meta"]):
#         tag.decompose()

#     return soup.get_text()


