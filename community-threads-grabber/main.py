import praw
import os
from datetime import datetime
import json
import requests

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
token = os.environ["GIST_TOKEN"]
gist_id = os.environ["GIST_ID"]
sub = "developersIndia"


def get_gist_content(gist_id):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    gist = response.json()
    filename = list(gist["files"].keys())[0]
    return gist["files"][filename]["content"]


def update_gist(gist_id, filename, content, description=""):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"description": description, "files": {filename: {"content": content}}}
    response = requests.patch(
        f"https://api.github.com/gists/{gist_id}", headers=headers, json=data
    )
    return response.json()


def get_collection(reddit):
    collection = reddit.subreddit(sub).collections(
        permalink="https://reddit.com/r/developersIndia/collection/958aef35-f9cb-414d-ab33-08bc639e47de"
    )
    return collection


def update_wiki(reddit, wikipage, posts):
    wiki_header = """# A collection of good discussions started by community members"""
    content = wiki_header + "\n\n"
    # given a wiki link, update the wiki page with new markdown
    wikipage = reddit.subreddit(sub).wiki[wikipage]

    for post in posts:
        formatted_date = datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y')
        content += f"- `{formatted_date}` [{post['title']}]({post['url']})\n\n"
    
    wikipage.edit(content=content)
    print("Wiki updated successfully!")


def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=f"Automod reader by u/{username}",
    )

    collection = get_collection(reddit)

    saved_collection_posts = json.loads(get_gist_content(gist_id))
    saved_collection_ids = [post["id"] for post in saved_collection_posts["posts"]]

    print(f"Database was last updated on {saved_collection_posts['collection_last_updated']}")
    print(f"Collection was last updated on {datetime.utcfromtimestamp(collection.last_update_utc).isoformat()}")

    if (
        saved_collection_posts["collection_last_updated"]
        != datetime.utcfromtimestamp(collection.last_update_utc).isoformat()
    ):
        print("Collection was updated, getting new posts data...")

        # given 2 lists find non-common elements
        db_posts = set(saved_collection_ids)
        collection_posts = []
        for submission in collection:
            collection_posts.append(submission.id)
        collection_posts = set(collection_posts)

        new_posts = list(collection_posts - db_posts)
        deleted_posts = list(db_posts - collection_posts)

        print(f"Found {len(new_posts)} new posts!")
        print(f"Found {len(deleted_posts)} deleted posts!")

        posts = []
        # load the saved collection posts data
        for submission_id in saved_collection_posts["posts"]:
            if submission_id["id"] in deleted_posts:
                continue
            post = {
                "title": submission_id["title"],
                "url": submission_id["url"],
                "id": submission_id["id"],
                "num_comments": submission_id["num_comments"],
                "created_at": submission_id["created_at"],
                "flair_text": submission_id["flair_text"],
            }
            posts.append(post)

        # get the new posts data
        for submission_id in new_posts:
            submission = reddit.submission(submission_id)
            post = {
                "title": submission.title,
                "url": submission.url,
                "id": submission.id,
                "num_comments": submission.num_comments,
                "created_at": datetime.utcfromtimestamp(
                    submission.created_utc
                ).isoformat(),
                "flair_text": submission.link_flair_text,
            }
            posts.append(post)

        # sort the posts by created_at
        posts = sorted(posts, key=lambda k: k["created_at"])

        collection_json = {
            "collection_last_updated": datetime.utcfromtimestamp(
                collection.last_update_utc
            ).isoformat(),
            "posts": posts,
        }

        update_gist(gist_id, "collection.json", json.dumps(collection_json, indent=4))
        print("Internal database updated successfully!")
        update_wiki(reddit, "community-threads", posts)
    else:
        print("Collection Saved data is up to date!")


if __name__ == "__main__":
    main()
