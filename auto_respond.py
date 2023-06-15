import arrow
import praw
import time
import requests
import config


# Create a Reddit instance
reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent="modmail_auto_responder_v0.1 fork by u/urielsalis",
    password=config.password,
    username=config.username,
)

# Define the list you want this to operate on.  A modmail conversation stream fetches ALL subreddits
allowed_subreddits = ["minecraft"]

# Define the list of keywords for the auto-respond trigger
keywords = [
    "request to join",
    "let me in",
    "access",
    "member",
    "private",
    "blackout",
    "dark",
    "closed",
    "join",
    "shutdown",
    "protest",
    "api",
    "third party",
    "3rd party",
    "spez",
    "apollo",
    "reddit is fun",
]

# Define the auto-response
main_response_message = """Hello /u/{author},

The subreddit r/Minecraft is currently set to private mode in protest of Reddit's changes to the API and will not be public again until Reddit Inc. accommodates for the Reddit community's needs. This decision was not taken lightly, but it was [voted upon by our community](https://imgur.com/qYbUaWT.png), who decided that this would be the right thing to do.
You can read more about this on r/Save3rdPartyApps or in [this topic](https://redd.it/1476ioa).

In the meantime, here are some links you may need:

**Information/Support:**
- [Minecraft Support, if you have problems with your account](https://help.minecraft.net/hc/)
- [Minecraft Community Support Discord server, if you need tech support involving the game itself](https://discord.gg/58Sxm23)
- [Minecraft Wiki, if you have a question about the game or are looking at how rare is a pink sheep](https://minecraft.fandom.com/)
- [Minecraft Bug Tracker, if you want to see if something in the game is normal or not](https://bugs.mojang.com/)

**Other Minecraft social platforms:**
- [The Minecraft Forum, if you want a place that can fill the Reddit-shaped hole in your heart](https://minecraftforum.net)
- [The official Minecraft Discord server](https://discord.gg/minecraft)

Best regards,
The r/Minecraft Team"""

processed_mail = set()

# Begin the main function of the bot.  The bot will need to be interrupted manually
while True:
    try:
        # Print something to the terminal so you know it's working.
        print(f"Logged in as {reddit.user.me()}...")
        print("Fetching modmail conversations...")
        for conv in reddit.subreddit("all").mod.stream.modmail_conversations(
            skip_existing=True
        ):
            # Check if the conversation owner is in the list of allowed subreddits
            if conv.owner not in allowed_subreddits:
                continue  # If not, skip the rest of this loop and move to the next conversation

            # Check if we've already processed this modmail.
            if conv.id not in processed_mail:
                # Check if the conversation only has the original message so the bot doesn't reply to messages further in the chain.
                if len(conv.messages) != 1:
                    continue

                # Check if the conversation started less than 24 hours ago
                if arrow.get(conv.last_updated) < arrow.utcnow().shift(hours=-24):
                    continue

                # Grab the subject of the first message in the conversation.
                modmail_subject = conv.subject.lower()

                # Get the body of theoriginal message
                original_message = conv.messages[0].body_markdown.lower()

                # Check for keywords in the message subject or body.
                search_text = original_message + modmail_subject
                for keyword in keywords:
                    if keyword in search_text:
                        print(
                            f"Found modmail in r/{conv.owner}  > {keyword} < in message from user {conv.user.name}"
                        )
                        # Reply and archive the message with the preset response, hide the username of the sender.
                        conv.reply(body=main_response_message.format(author=conv.user.name), author_hidden=True)
                        conv.archive()
                        # Add the id of the conversation to a set so it won't be checked again.
                        processed_mail.add(conv.id)
                        print(
                            f"Replied to message ID {conv.id} from user {conv.user.name} with the preset response\n"
                        )

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Sleeping for 60 seconds before retrying...")
        time.sleep(60)
