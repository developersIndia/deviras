import os
import sys
import praw


client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
sub = "developersIndia"


def assign_user_flair(reddit, username, flair_text):
    subreddit = reddit.subreddit(sub)
    flair = next(subreddit.flair(username))

    template = get_flair_template_from_text(reddit, flair['flair_text'])
    subreddit.flair.set(username, text=flair_text, flair_template_id=template['id'])

def get_flair_templates(reddit):
    subreddit = reddit.subreddit(sub)
    return subreddit.flair.templates


def get_flair_template_from_text(reddit, flair_text):
    templates = get_flair_templates(reddit)
    for template in templates:
        if template['text'] == flair_text:
            return template


def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=f"Automod reader by u/{username}",
    )

    if len(sys.argv) != 3:
        print("Usage: python main.py <username> <flair_text>")
        sys.exit(1)

    # get username from CLI args
    reddit_username = sys.argv[1]
    # get flair text from CLI args
    flair_text = sys.argv[2]

    assign_user_flair(reddit, reddit_username, flair_text)


if __name__ == "__main__":
    main()