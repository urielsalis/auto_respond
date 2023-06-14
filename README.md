
Modmail Auto-Responder Bot

This script creates a Reddit bot that auto-responds to Modmail messages that contain specific keywords in the message subject or body. It utilizes the Python Reddit API Wrapper (PRAW) to interact with Reddit's API.
Features

    The bot operates on a specific list of subreddits.
    It responds to Modmail messages containing any of the keywords defined in a list.
    The bot archives the conversation after sending the response.
    It records which Modmail conversations it has replied to, to avoid sending multiple responses to the same conversation.
    If a Modmail message comes from an admin, the bot will send a private message to every moderator of the subreddit, notifying them of the admin Modmail.

Requirements

    Python 3
    PRAW: Python Reddit API Wrapper

To install PRAW, run:

bash

pip install praw

Usage

    Clone the repository:

bash

git clone https://github.com/yourusername/auto_respond.git
cd auto_respond

    You need to have a config.py file in your project directory with your Reddit app credentials:

python

client_id = 'your_client_id'
client_secret = 'your_client_secret'
refresh_token = 'your_refresh_token'

    Run the script:

bash

python3 auto_respond.py

Configuring the Bot

You can customize the bot's behavior by modifying the following variables in the auto_respond.py script:

    allowed_subreddits: List of subreddits the bot should operate on.
    keywords: List of keywords the bot should respond to.
    main_response_message: The message the bot should send in response to matching Modmail messages.

Contributing

We appreciate your contributions! Please fork this repository, make your changes, and submit a pull request. If you have any questions or need help, feel free to open an issue.
Disclaimer

This bot should be used responsibly and in accordance with Reddit's API Terms of Service. The creator of this bot is not responsible for any misuse or damage caused by this bot.

Remember to replace "yourusername" with your actual GitHub username in the "Clone the repository" step, and feel free to customize this README to better suit your project.