import datetime
import praw
import os

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = 'Showcase Sunday Megathread'
sub = "developersIndia"

def is_second_sunday():
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    day_of_week = first_day_of_month.weekday()
    # Calculate the date of the second Sunday
    second_sunday = first_day_of_month + datetime.timedelta(days=(6 - day_of_week + 7) % 7 + 7)
    return today == second_sunday


def create_showcase_sunday_megathread(subreddit):
    flair = next(
        filter(
            lambda flair: "Showcase Sunday" in flair["flair_text"],
            subreddit.flair.link_templates.user_selectable(),
        )
    )
       
    title = "Showcase Sunday Megathread - {month} {year}".format(month=datetime.date.today().strftime("%B"), year=datetime.date.today().year)
    text = """
It's time for our monthly showcase thread where we celebrate the incredible talent in our community. Whether it's an app, a website, a tool, or anything else you've built, we want to see it! Share your latest creations, side projects, or even your work-in-progress. Ask for feedback, and help each other out.

Let's inspire each other and celebrate the diverse skills we have. Comment below with details about what you've built, the tech stack used, and any interesting challenges faced along the way.

### [Looking for more projects built by developersIndia community members?](https://www.reddit.com/r/developersIndia/?f=flair_name%3A%22I%20Made%20This%20%3Asnoo_wink%3A%22)

**Showcase Sunday thread is posted on the second Sunday of every month. You can find the [schedule on our calendar](https://developersindia.in/events-calendar). You can also find past [showcase sunday megathreads here](https://www.reddit.com/r/developersIndia/?f=flair_name%3A%22Showcase%20Sunday%20%3Asnoo_hearteyes%3A%22)**.
"""

    submission = subreddit.submit(
        title,
        selftext=text,
        flair_id=flair["flair_template_id"],
    )
    submission.mod.approve()
    submission.mod.sticky()
    submission.mod.distinguish()

    return submission

def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit(sub)

    if is_second_sunday():
        create_showcase_sunday_megathread(subreddit)
        print("Showcase Sunday Megathread created successfully!")
    else:
        print("Skipping. Not the second Sunday of the month")

if __name__ == "__main__":
    main()