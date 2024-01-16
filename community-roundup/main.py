import datetime
import praw
import os
import json
import requests

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = "Community Roundup Post"
token = os.environ["GIST_TOKEN"]
gist_id = os.environ["GIST_ID"]
sub = "developersIndia"


def is_last_day_of_month():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.day == 1


def get_gist_content(gist_id):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    gist = response.json()
    filename = list(gist["files"].keys())[0]
    return gist["files"][filename]["content"]


def get_monthly_roundup():
    saved_collection_posts = json.loads(get_gist_content(gist_id))
    # filter posts for this month & year
    saved_collection_posts = list(
        filter(
            lambda post: datetime.datetime.strptime(
                post["created_at"], "%Y-%m-%dT%H:%M:%S"
            ).year == datetime.date.today().year and
            datetime.datetime.strptime(
                post["created_at"], "%Y-%m-%dT%H:%M:%S"
            ).month == datetime.date.today().month,
            saved_collection_posts["posts"],
        )
    )
    return saved_collection_posts


def create_community_roundup_post(subreddit, posts):
    flair = next(
        filter(
            lambda flair: "Community Roundup" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    title = "Community Roundup: List of must read posts & discussions that happened this month - {month} {year}".format(
        month=datetime.date.today().strftime("%B"), year=datetime.date.today().year
    )

    text = "|||"
    text += "\n|--------|--------|\n"
    footer_text = """\n\n
---

**Community Roundup is posted on the last day of every month. You can find the [schedule on our events calendar](https://developersindia.in/events-calendar). To find the list of all [interesting posts & community threads over time, checkout our wiki](https://www.reddit.com/r/developersIndia/wiki/community-threads/).\n**
If you think we missed any interesting post or discussion, please share it with us via modmail.
"""
    posts_counter = 0
    for post in posts:
        posts_counter += 1
        text += f"| {posts_counter} | [**{post['title']}**]({post['url']}) |\n"

    text = text + footer_text

    submission = subreddit.submit(
        title,
        selftext=text,
        flair_id=flair["flair_template_id"],
    )
    submission.mod.approve()
    submission.mod.sticky()
    submission.mod.distinguish()
    submission.mod.lock()

    return submission


def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=user_agent,
    )

    subreddit = reddit.subreddit(sub)

    if is_last_day_of_month():
        posts = get_monthly_roundup()
        if len(posts) == 0:
            print("No posts found in the collection for this month. Skipping")
            return
        create_community_roundup_post(subreddit, posts)
        print("Community Roundup post created successfully!")
    else:
        print("Skipping. Not the last day of the month")


if __name__ == "__main__":
    main()
