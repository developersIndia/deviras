'''
    This script is used for changing the text below total members & live
    members count in the developersIndia subreddit
'''
import praw
import os
import random
import time
import json

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]

def get_titles():
    with open('idcard_update/dataset.json', 'r') as f:
        data = json.load(f)

    titles = data['titles']
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

if __name__ == '__main__':
    update_titles()
