# James: Voice and Text Interaction with Chat GPT

**James** is a CLI (command-line interface) for interacting with OpenAI's Chat GPT using voice and text. 

Main functionality: 

- ask questions via Voice and James reads it aloud
- automatically copy Code from answers to the clipboard  
- save answers to files 
- append text and code files to your prompt
- fetch news articles from various sources (Hacker News, CNN, etc.) and generate summarized versions of them

With more to come... 

## Prerequisites

- Python 3.8+
- A working installation of `pip`
- A valid `API key` for OpenAI
- (optional) A valid `API key` and `API secret` for UberDuck

## Installation

1. Clone the repository `git clone git@github.com:guarilha/james.git` and `cd james`.

2. Install the required dependencies using `pip`:

   ```
   pip install -r requirements.txt
   ```

3. Install the local package using `pip`:
    
   ```
   pip install -e .
   ```

## Usage

### General Help

```
james --help
```

### `ask` Command

Interact with Chat GPT using voice and text.

```
james ask [OPTIONS]
```

Options:

- `--question, -q QUESTION`: Bypass capturing the mic audio and speech to text.
- `--character, -c CHARACTER`: A profession, a name of a famous person, or from fiction (movies, series, etc.).
- `--play, -p PLAY`: Read aloud the answer at the end. Options are: tts, uberduck.
- `--file, -f FILE`: Upload a text or code file at the end of your prompt.
- `--save, -s SAVE`: Save the answer to a file.
- `--no-clipboard, -b`: Avoid copying code content to the clipboard.

### `news` Command

Fetch news articles from sources and generate summaries.

```
james news [OPTIONS]
```

Options:

- `--category, -c CATEGORY`: Search from Hacker News or selected news sites (CNN, etc.).
- `--number, -n NUMBER`: Number of news articles you want to fetch.
- `--position, -p POSITION`: Fetch news at a specific position.
- `--is-list, -l`: Avoid news summaries and only print a list.

## Examples

### Speak a question and get the response from Chat GPT.

```
james ask
```

### Ask a question directly.

```
james ask -q "What is the meaning of life?"
```

### Ask a question as a specific character, e.g., Elon Musk.

```
james ask -q "How do you stay inspired?" -c "Elon Musk"
```

### Read aloud the answer.

```
james ask -q "How do you solve a coding problems?" -p tts
james ask -q "How do you solve a coding problems?" -p uberduck
```

### Upload a file with your question.

```
james ask -q "Review this code" -f sample_code.py
```

### Save the answer to a file.

```
james ask -q "What is the best way to learn Python?" -s answer.txt
```

### Get top news from Hacker News.

```
james news
james news -c hackernews
```

### Get a list of tech news articles for a category.

```
james news -c "business and finance" -l
```

### Get a summary of the article at a specific position from Hacker News.

```
james news -p 5
```

### Get a list of political news articles and avoid summaries.

```
james news -c "politics" --is-list
```