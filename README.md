# Claude CLI Chatbot

A beginner-friendly Python CLI chatbot built with the official Anthropic API.

This project was created to practice working with Claude through the Anthropic API. It includes conversation memory, JSON saving, streaming responses, strict answer evaluation, cost control with `max_tokens`, and clean terminal formatting with `rich`.

## Features

- Chat with Claude from the terminal
- Uses the official `anthropic` Python library
- Loads API key safely from `.env`
- Uses `.venv` virtual environment
- Streams Claude responses live
- Saves conversation history to `conversation.json`
- Keeps only the last 20 messages to control context size
- Includes strict `/evaluate` command for Claude-output evaluation practice
- Includes useful CLI commands: `/help`, `/history`, `/save`, `/reset`, `/evaluate`, `/exit`
- Uses `rich` for clean terminal formatting
- Handles common Anthropic API errors

## Project Setup

Create and open the project folder:

    cd ~/Desktop
    mkdir anthropic-api-practice
    cd anthropic-api-practice
    code .

Create a virtual environment:

    python3 -m venv .venv

Activate the virtual environment:

    source .venv/bin/activate

Install packages:

    pip install anthropic python-dotenv rich

## Environment Variables

Create a `.env` file in the project root and add:

    ANTHROPIC_API_KEY=your_api_key_here

Do not share your `.env` file publicly.

## Run the Chatbot

Run:

    python chatbot.py

## Commands

Use these commands inside the chatbot:

    /help
    /history
    /save
    /reset
    /evaluate
    /exit

## What I Learned

- How to use the official Anthropic Python SDK
- How to call Claude with `client.messages.create()`
- How to stream Claude responses
- How to use system prompts
- How to manage conversation history
- How to save and load JSON memory
- How to control cost with `max_tokens`
- How to handle common API errors
- How to build a practical CLI chatbot
- How to evaluate Claude-style answers strictly

