import praw
import os
import random
import time

titles = [
    "ranting about jira",
    "siting in a meeting",
    "squashing bugs",
    "centering divs",
    "waiting for staging deployment",
    "writing tests",
    "pushing directly to prod",
    "doing code review",
    "deleting jira tickets",
    "Creating a pull request",
    "forgot to run DB migrations",
    "Broke production",
    "running on staging ENV",
    "merging git branches",
    "releasing the MVP",
    "finding JIRA tickets"
]

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]

def get_titles():
    currentlyViewingText, subscribersText = random.sample(titles, 2)
    return [currentlyViewingText, subscribersText]


def update_titles():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=reddit_pass,
        user_agent="testscript by u/BhupeshV",
        username="BhupeshV",
    )
    widgets = reddit.subreddit("developersIndia").widgets
    id_card = widgets.id_card
    print("Titles Before update")
    # total members
    print(id_card.subscribersText)
    print(id_card.currentlyViewingText)

    titles = get_titles()
    print(titles)

    widgets.id_card.mod.update(currentlyViewingText=titles[0])
    widgets.refresh()
    widgets.id_card.mod.update(subscribersText=titles[1])

update_titles()