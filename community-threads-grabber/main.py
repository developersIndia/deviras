import praw
import os
from datetime import datetime
import json

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]


def get_collection(reddit):
    collection = reddit.subreddit("developersIndia").collections(
        permalink="https://reddit.com/r/developersIndia/collection/958aef35-f9cb-414d-ab33-08bc639e47de"
    )
    return collection


def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=f"Automod reader by u/{username}",
    )

    collection = get_collection(reddit)

    print(f"Last updated: {datetime.utcfromtimestamp(collection.last_update_utc)}")

    posts = []

    for submission_id in collection.sorted_links:
        submission = reddit.submission(submission_id)
        post = {
            "title": submission.title,
            "url": submission.url,
            "id": submission.id,
            "num_comments": submission.num_comments,
            "created_at": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
            "flair_text": submission.link_flair_text,
        }
        posts.append(post)

    collection_json = {
        "collection_last_updated": datetime.utcfromtimestamp(
            collection.last_update_utc
        ).isoformat(),
        "posts": posts,
    }

    with open("collection.json", "w") as f:
        json.dump(collection_json, f, indent=4)


if __name__ == "__main__":
    main()
