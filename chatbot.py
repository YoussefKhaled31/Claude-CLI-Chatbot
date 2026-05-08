from curses import error
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

load_dotenv()

console = Console()

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 500
MEMORY_LIMIT = 20
MEMORY_FILE = Path("conversation.json")

client = anthropic.Anthropic()

def load_memory():
    if not MEMORY_FILE.exists():
        return[]
    try:
        with MEMORY_FILE.open("r", enconding="utf-8") as file:
            messages = json.load(file)
        if isinstance(messages, list):
            return messages[-MEMORY_LIMIT:]
        
        return[]
    
    except json.JSONDecodeError:
        console.print(Panel("conversation.json is broken. Starting with empty memory.", border_style="blue"))
        return[]
    
def save_memory(messages):
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(messages[-MEMORY_LIMIT:], file, indent=2)

def show_help():
    table = Table(title="Claude CLI Commands")
    table.add_column("Command", style="cyan")
    table.add_column("What it does")
    table.add_row("/help", "Show available commands.")
    table.add_row("/history", "Show the current conversation memory.")
    table.add_row("/save", "Save the current conversation to conversation.json.")
    table.add_row("/reset", "Clear the conversation memory.")
    table.add_row("/evaluate", "Strictly evaluate a Claude-style answer.")
    table.add_row("/exit", "Save and exit the chatbot.")

    console.print(table)

def show_history(messages):
    if not messages:
        console.print(Panel("No conversation history yet.", border_style="yellow"))
        return
    
    table = Table(title="Conversation History")
    table.add_column("#")
    table.add_column("Role")
    table.add_column("Content")

    for index, message in enumerate(messages, start=1):
        content = message["content"]

        if len(content) > 120:
            content = content[:120] + "..."
        
        table.add_row(str(index), message["role"], content)

    console.print(table)

def ask_multiline(title):
    console.print(Panel("Paste your text below. Type END on its own line when finished.",
    title=title, border_style="cyan"))
    
    lines = []

    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)

    return "\n".join(lines).strip()

def evaluate_answer():
    user_instruction = ask_multiline("Original User Instruction")
    claude_answer = ask_multiline("Claude Answer To Evaluate")

    if not user_instruction or not claude_answer:
        console.print(Panel("Both the instruction and answer are required.",
        border_style="red"))
        return

    evlaution_prompt = f"""
You are a strict AI output evaluator preparing someone for professional Claude-output review work.

Evaluate the answer harshly but fairly.

Original user instruction:
<instruction>
{user_instruction}
</instruction>

Claude answer:
<answer>
{claude_answer}
</answer>   

Return the evaluation in this structure:

# Evaluation Report

## Overall Score
Give a score from 1 to 10.

## Instruction-Following Score
Give a score from 1 to 10 and explain why.

## Clarity Score
Give a score from 1 to 10 and explain why.

## Accuracy/Support Score
Give a score from 1 to 10 and explain whether the answer makes unsupported claims.

## Strengths
List the strongest parts.

## Weaknesses
List the biggest problems.

## Missing Details
List what should have been included.

## Final Verdict
Be direct. Say whether this answer would pass a strict evaluation.

## Suggested Improved Answer
Rewrite the answer better.
"""
    

    try:
        console.print(Panel("Claude is evaluating the answer...", border_style="yellow"))
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system="You are a strict, professional AI response evaluator. Do not overpraise weak answers.",
            messages=[
                {
                    "role": "user",
                    "content": evaluation_prompt,
                }
            ],
        )
        report = response.content[0].text
        console.print(Panel(Markdown(report), title="Strict Evaluation Report", border_style="green"))
    except anthropic.AuthenticationError:
        console.print(Panel("Authentication failed. Check your ANTHROPIC_API_KEY in .env.", border_style="red"))
    except anthropic.RateLimitError:
        console.print(Panel("Rate limit reached. Try again later.", border_style="red"))
    except anthropic.NotFoundError:
        console.print(Panel("Model not found. Check the MODEL value.", border_style="red"))
    except anthropic.APIConnectionError:
        console.print(Panel("Connection error. Check your internet.", border_style="red"))
    except anthropic.APIStatusError as error:
        console.print(Panel(f"API error: {error.status_code}", border_style="red"))
    except Exception as error:
        console.print(Panel(f"Unexpected error: {error}", border_style="red"))
        