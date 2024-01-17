import os
import sys
import praw
import datetime

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
sub = "developersIndia"


def get_last_activity_times(reddit, username):
    user = reddit.redditor(username)

    # Get the user's last comment time in the subreddit
    last_comment_time = None
    for comment in user.comments.new(
        limit=100
    ):  # look at the user's 100 most recent comments
        if comment.subreddit.display_name == sub:
            last_comment_time = datetime.datetime.fromtimestamp(comment.created_utc)
            break

    # Get the user's last post creation time and title in the subreddit
    last_post_time = None
    last_post_title = None
    for submission in user.submissions.new(
        limit=100
    ):  # look at the user's 100 most recent posts
        if submission.subreddit.display_name == sub:
            last_post_time = datetime.datetime.fromtimestamp(submission.created_utc)
            last_post_title = submission.title
            break

    return last_comment_time, last_post_time, last_post_title


def assign_user_flair(reddit, username, flair_text):
    subreddit = reddit.subreddit(sub)
    flair = next(subreddit.flair(username))

    template = get_flair_template_from_text(reddit, flair["flair_text"])
    subreddit.flair.set(username, text=flair_text, flair_template_id=template["id"])


def get_flair_templates(reddit):
    subreddit = reddit.subreddit(sub)
    return subreddit.flair.templates


def get_flair_template_from_text(reddit, flair_text):
    templates = get_flair_templates(reddit)
    for template in templates:
        if template["text"] == flair_text:
            return template


def send_message(reddit, username, flair_text):
    message_subject = 'Woohoo! You are now a verified member of r/developersIndia! 🚀'
    message_text = """
Hi there,\n
As requested your user-flair has now been updated to a verified version. You now have the **{flair}** flair on r/developersIndia ✨\n

This means that you are now a trusted member of the community and we hope that you will continue to contribute to the community in a positive way. \n

As a reminder,\n
- Make sure to follow [Code of Conduct](https://developersindia.in/code-of-conduct/) before participating in discussions.
- Go through [rules](https://www.reddit.com/r/developersIndia/wiki/community-rules/) before creating a new post.\n
If you know someone who is active on r/developersIndia, please send them this [wiki on how to get verified](https://www.reddit.com/r/developersIndia/wiki/verified-flair)\n

\n\n
PS: This was an automated messaage, no need to reply. [Reach out to mods](https://www.reddit.com/message/compose?to=/r/developersIndia) if you have any questions.

Namaste 🙏
"""
    reddit.redditor(username).message(
        subject=message_subject, message=message_text.format(flair=flair_text), from_subreddit=reddit.subreddit(sub)
    )


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

    # get last activity times
    last_comment_time, last_post_time, last_post_title = get_last_activity_times(reddit, reddit_username)
    if last_comment_time is not None:
        print(f"{reddit_username}'s last comment time on developersIndia was {last_comment_time}")
    if last_post_time is not None:
        print(f"{reddit_username}'s last post on developersIndia was \"{last_post_title}\" on {last_post_time}")

    assign_user_flair(reddit, reddit_username, flair_text)
    send_message(reddit, reddit_username, flair_text)


if __name__ == "__main__":
    main()
