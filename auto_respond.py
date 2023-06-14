import praw
import time
import requests
import config


# Create a Reddit instance
reddit = praw.Reddit(
	client_id = config.client_id,
	client_secret = config.client_secret,
	user_agent="modmail_auto_responder_v0.1 by u/buckrowdy",
	refresh_token =config.refresh_token,
)

# Define the list you want this to operate on.  A modmail conversation stream fetches ALL subreddits
allowed_subreddits = ["YOUR_SUBREDDITS_HERE", "AS_A_LIST"]

# Define the list of keywords for the auto-respond trigger
keywords = ['request to join','let me in', 'access', 'member', 'private', 'blackout', 'dark', 'closed', 'join', 'shutdown,']

# Define the auto-response
main_response_message =f"Hello and thank you...[YOUR_MESSAGE_HERE]" 

# Set up a list to hold IDs of modmail the bot has already replied to.
processed_mail = []

# Begin the mnain function of the bot.  The bot will need to be interrupted manually
while True:
    try:
        # Print something to the terminal so you know it's working.
        print(f"Logged in as {reddit.user.me()}...")
        print("Fetching modmail conversations...")
        for conv in reddit.subreddit('all').mod.stream.modmail_conversations(skip_existing=True):
            # Check if the conversation owner is in the list of allowed subreddits
            if conv.owner not in allowed_subreddits:
                continue  # If not, skip the rest of this loop and move to the next conversation
         
            # This specific condition will send a PM top every mod on the team if an admin modmail is sent so you don't miss it.
            if len([author for author in conv.authors if author.is_admin]) > 0:
                # Utilize u/mod_mailer, a mail relay bot.
                reddit.redditor("mod_mailer").message(subject=f"{conv.owner}", message =f"New Admin modmail in r/{conv.owner}\n\n---\n\nNew modmail message from admins https://mod.reddit.com/mail/all/{conv.id}\n\nSubject: {conv.subject}")
                conv.archive()

            # Check if we've already processed this modmail.
            if conv.id not in processed_mail:
                # Grab the subject of the first message in the conversation.
                modmail_subject = conv.subject.lower()

                # Check if the conversation only has the original message so the bot doesn't reply to messages further in the chain.
                if len(conv.messages) != 1:
                    continue

                # Get the body of theoriginal message
                original_message = conv.messages[0].body_markdown.lower()

                # Check for keywords in the message subject or body.
                if any(keyword in original_message for keyword in keywords) or any(keyword in modmail_subject for keyword in keywords):
                    print(f"Found modmail in r/{conv.owner}  > {keyword} < in message from user {conv.user.name}")
                    # Reply and archive the message with the preset response, hide the username of the sender.
                    conv.reply(body=response_message, author_hidden=True)
                    conv.archive()
                    # Add the id of the conversation to a list so it won't be checked again.
                    processed_mail.append(conv.id)
                    print(f"Replied to message ID {conv.id} from user {conv.user.name} with the preset response\n")
                 
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Sleeping for 60 seconds before retrying...")
        time.sleep(60)
