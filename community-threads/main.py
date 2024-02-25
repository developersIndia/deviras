import praw
import os
import argparse
from datetime import datetime
import json
from collections import defaultdict 
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

# farewell, reddit collections
# def get_collection(reddit):
#     collection = reddit.subreddit(sub).collections(
#         permalink="https://reddit.com/r/developersIndia/collection/958aef35-f9cb-414d-ab33-08bc639e47de"
#     )
#     return collection

def get_post_data(reddit, post_url):
    submission = reddit.submission(url=post_url)
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
    return post

def update_wiki(reddit, wikipage, posts):
    # Group posts by year
    posts_by_year = defaultdict(list)
    for post in posts:
        year = datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S').year
        posts_by_year[year].append(post)

    # Sort posts within each year
    for year in posts_by_year:
        posts_by_year[year] = sorted(posts_by_year[year], key=lambda k: k['created_at'], reverse=True)

    # Calculate total posts and years
    total_posts = sum(len(posts) for posts in posts_by_year.values())
    total_years = len(posts_by_year)

    wiki_header = """# A collection of must read discussions started by community members"""
    content = wiki_header + "\n\n"
    content += f"A handpicked collection of **{total_posts}** interesting posts, discussions & high-quality threads gathered over **{total_years-1}** years & counting.\n\n"
    content += "If you spot a post that could be in this list, send us a [modmail](https://reddit.com/message/compose?to=r/developersIndia&subject=Community%20Threads%20Collection%20Suggestion&message=Hey%20folks%2C%0A%0A%3Cpost%20link%3E)\n\n"

    for year in sorted(posts_by_year.keys(), reverse=True):
        content += f"## {year}\n\n"
        # Add the posts for this year
        for post in posts_by_year[year]:
            formatted_date = datetime.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%d %b, %Y')
            content += f"- `{formatted_date}` [**{post['title']}**]({post['url']})\n\n"
    
    # given a wiki link, update the wiki page with new markdown
    wikipage = reddit.subreddit(sub).wiki[wikipage]
    wikipage.edit(content=content)
    print("Wiki updated successfully!")


def main():
    parser = argparse.ArgumentParser(description='Update Community Threads Collection.')
    parser.add_argument('post_url', help='The URL of the Reddit post to add.')
    args = parser.parse_args()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=f"Automod reader by u/{username}",
    )

    saved_collection_posts = json.loads(get_gist_content(gist_id))
    saved_collection_ids = [post["id"] for post in saved_collection_posts["posts"]]

    print(f"Database was last updated on {saved_collection_posts['collection_last_updated']}")

    posts = []
    for submission_id in saved_collection_posts["posts"]:
        post = {
            "title": submission_id["title"],
            "url": submission_id["url"],
            "id": submission_id["id"],
            "num_comments": submission_id["num_comments"],
            "created_at": submission_id["created_at"],
            "flair_text": submission_id["flair_text"],
        }
        posts.append(post)

    new_post = get_post_data(reddit, args.post_url)
    if new_post["id"] not in saved_collection_ids:
        posts.append(new_post)
        posts = sorted(posts, key=lambda k: k["created_at"])

        collection_json = {
            "collection_last_updated": datetime.utcnow().isoformat(),
            "posts": posts,
        }

        update_gist(gist_id, "collection.json", json.dumps(collection_json, indent=4))
        print("Internal database updated successfully!")
        update_wiki(reddit, "community-threads", posts)
    else:
        print("Post is already in the collection. No changes were made.")


if __name__ == "__main__":
    main()
