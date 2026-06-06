# LinariBot

## Description
LinariBot is a Telegram bot designed for the [Linari](https://t.me/linari_me) community. The bot welcomes new members and enforces community rules by restricting users until they accept the guidelines.


## Features
- Greets new members with rules and restrictions
- Restricts users until they accept the community rules
- Russian language interface
- Throttling middleware to prevent spam
- Uses singleton pattern for bot instance
- Works with a Telegram channel

## Prerequisites
- Python 3.8 or higher
- uv 0.11.16 or higher

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kiNgchev/linari-bot.git
   ```
2. Sync the uv project:
   ```bash
   uv sync
   ```

## Configuration
Set up the following environment variables:
- `TOKEN` – Telegram bot token
- `CHANNEL_ID` – Telegram channel ID, which the bot should be subscribed to
- `CHAT_ID` – Telegram chat ID where the bot should operate


## Usage
Run the bot:
   ```bash
   uv run src/main.py
   ```
## Deployment
Use the provided Dockerfile to containerize the application for deployment.
Follow the instructions in the Dockerfile to build and run the Docker image.

## License
This project is licensed under the MIT License. See the LICENSE file for details.