import praw
import os

# Reddit API credentials
client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = "Wiki Mention Notifier"
sub = "developersIndia"

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=reddit_pass,
    user_agent=user_agent,
    username=username,
)

def send_message(reddit, username):
    message_subject = 'Woohoo! Your advice/perspective is now part of our wiki!'
    message_text = """
Hi there,\n
It looks like one of your comments on r/developersIndia was picked-up by the volunteer team to be part of our [community-driven wiki](https://wiki.developersindia.in/).\n

- You can find your advice by searching your username in our [Wiki](https://wiki.developersindia.in/).\n
- We can't thank you enough for your valuable contribution to our community 🧡\n\n

Please keep contributing productively!\n

Cheers,\n
The r/developersIndia Community Team
"""
    reddit.redditor(username).message(
        subject=message_subject, message=message_text, from_subreddit=reddit.subreddit(sub)
    )


def add_mod_note_good_contributor(reddit, username):
    subreddit = reddit.subreddit(sub)
    subreddit.mod.notes.create(
        redditor=username,
        label="HELPFUL_USER",
        note="Their advice/perspective was mentioned in our wiki.",
    )

def main():
    if len(os.sys.argv) != 2:
        print("Usage: python main.py <username>")
        return

    reddit_username = os.sys.argv[1]

    send_message(reddit, reddit_username)
    add_mod_note_good_contributor(reddit, reddit_username)
    print(f"Sent wiki mention modmail to {reddit_username}")

if __name__ == "__main__":
    main()