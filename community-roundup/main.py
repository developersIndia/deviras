import datetime
import praw
import os
import sys
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


def get_posts_by_flair(subreddit, flair):
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    posts = []
    for post in subreddit.search(f'flair_name:"{flair}"', time_filter="month"):
        post_date = datetime.datetime.fromtimestamp(post.created_utc)
        if post_date.year == current_year and post_date.month == current_month:
            post.title = post.title.replace("|", "\\|")  # Escape the "|" character
            posts.append(post)

    posts = sorted(posts, key=lambda post: post.created_utc, reverse=True)
    return posts


def get_weekly_discussion_posts(subreddit):
    flair = next(
        filter(
            lambda flair: "Weekly Discussion" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    return get_posts_by_flair(subreddit, flair["flair_text"])


def get_ama_posts(subreddit):
    flair = next(
        filter(
            lambda flair: "AMA" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    return get_posts_by_flair(subreddit, flair["flair_text"])


def get_i_made_this_posts(subreddit):
    flair = next(
        filter(
            lambda flair: "I Made This" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    # Get all posts with the specified flair
    posts = get_posts_by_flair(subreddit, flair["flair_text"])

    # Sort the posts by upvotes and then comments in descending order
    posts = sorted(
        posts, key=lambda post: (post.score, post.num_comments), reverse=True
    )

    # Return only the top 10 posts
    return posts[:10]


def get_announcement_posts(subreddit):
    flair = next(
        filter(
            lambda flair: "Announcement" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    return get_posts_by_flair(subreddit, flair["flair_text"])


def code_collaboration_posts(subreddit):
    flair = next(
        filter(
            lambda flair: "Code Collab" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    return get_posts_by_flair(subreddit, flair["flair_text"])

def get_gist_content(gist_id):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    gist = response.json()
    filename = list(gist["files"].keys())[0]
    return gist["files"][filename]["content"]


def get_community_threads():
    saved_collection_posts = json.loads(get_gist_content(gist_id))
    # filter posts for this month & year
    saved_collection_posts = list(
        filter(
            lambda post: datetime.datetime.strptime(
                post["created_at"], "%Y-%m-%dT%H:%M:%S"
            ).year
            == datetime.date.today().year
            and datetime.datetime.strptime(
                post["created_at"], "%Y-%m-%dT%H:%M:%S"
            ).month
            == datetime.date.today().month,
            saved_collection_posts["posts"],
        )
    )
    return saved_collection_posts


def create_community_roundup_post(
    subreddit,
    posts,
    i_made_this_posts,
    weekly_discussion_posts,
    ama_posts,
    announcement_posts,
    collab_posts,
):
    flair = next(
        filter(
            lambda flair: "Community Roundup" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    title = "Community Roundup: List of must read posts & discussions that happened this month - {month} {year}".format(
        month=datetime.date.today().strftime("%B"), year=datetime.date.today().year
    )

    footer_text = """\n\n
---

**Community Roundup is posted on the last day of each month. To explore a compilation of all interesting posts and community threads over time, [visit our wiki](https://www.reddit.com/r/developersIndia/wiki/community-threads/).**\n
The collection is curated by our volunteer team & is independent of the number of upvotes and comments (except for "I made This" posts). If you believe we may have overlooked any engaging posts or discussions, please share them with us via [modmail](https://reddit.com/message/compose?to=r/developersIndia&subject=Community%20Threads%20Collection%20Suggestion&message=Hey%20folks%2C%0A%0A%3Cpost%20link%3E).\n
"""

    if len(announcement_posts) > 0:
        text = "## Announcements\n|Announcements from volunteer team|\n|--------|\n"
        for post in announcement_posts:
            text += f"| [**{post.title.strip()}**]({post.url}) |\n"
    else:
        print("No announcements found. Skipping")

    if len(ama_posts) > 0:
        text += "\n## AMAs\n|Read insights from guests that joined us for a day |\n|--------|\n"
        for post in ama_posts:
            text += f"| [**{post.title.strip()}**]({post.url}) |\n"
    else:
        print("No AMAs found. Skipping")

    if len(posts) > 0:
        text += "\n## Community Threads\n|S.No|Insightful discussions started by community members|\n|--------|--------|\n"
        posts_counter = 0
        for post in posts:
            posts_counter += 1
            text += f"| {posts_counter} | [**{post['title']}**]({post['url']}) |\n"
    else:
        print("No posts found in the collection for this month. Skipping")

    if len(weekly_discussion_posts) > 0:
        text += "\n## Weekly Discussions\n|Weekly tech discussions started by Volunteer Team|\n|--------|\n"
        for post in weekly_discussion_posts:
            text += f"| [**{post.title.strip()}**]({post.url}) |\n"
    else:
        print("No weekly discussions found. Skipping")
    
    if len(collab_posts) > 0:
        text += "\n## Code Collab\n|Folks looking for collaborations on hackathons, projects etc.|\n|--------|\n"
        for post in collab_posts:
            text += f"| [**{post.title.strip()}**]({post.url}) |\n"
    else:
        print("No Code Collaboration posts found. Skipping")

    if len(i_made_this_posts) > 0:
        text += "\n## I Made This\n|Top 10 projects built by community members|\n|--------|\n"
        for post in i_made_this_posts:
            text += f"| [**{post.title.strip()}**]({post.url}) |\n"
    else:
        print("No I Made This posts found. Skipping")

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
        posts = get_community_threads()
        i_made_this_posts = get_i_made_this_posts(subreddit)
        weekly_discussion_posts = get_weekly_discussion_posts(subreddit)
        ama_posts = get_ama_posts(subreddit)
        announcement_posts = get_announcement_posts(subreddit)
        collab_posts = code_collaboration_posts(subreddit)
        create_community_roundup_post(
            subreddit, posts, i_made_this_posts, weekly_discussion_posts, ama_posts, announcement_posts, collab_posts
        )
        print("Community Roundup post created successfully!")
    else:
        print("Skipping. Not the last day of the month")


if __name__ == "__main__":
    main()
