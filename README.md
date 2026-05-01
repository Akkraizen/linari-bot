# LinariBot

## Description
LinariBot is a Telegram bot designed to [Linari](https://t.me/linari_me) community.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linari-bot.git
   ```
2. Create a virtual environment:
   - With python 
   ```bash
   python -m venv .venv
   ```
   - With python3
   ```bash
    python3 -m venv .venv
    ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source .venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the bot:
   ```bash
   python bot.py
   ```

## Configuration
Set up the next environment variables:
- `TOKEN` – Telegram bot token.
- `CHANNEL_ID` – Telegram channel ID, which the bot should be subscribed to.

## Deployment
Use the provided Dockerfile to containerize the application for deployment.
Follow the instructions in the Dockerfile to build and run the Docker image.

## License
This project is licensed under the MIT License. See the LICENSE file for details.