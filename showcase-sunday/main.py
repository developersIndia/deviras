import datetime
import praw
import os

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = 'Showcase Sunday Megathread'

def is_second_sunday():
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    day_of_week = first_day_of_month.weekday()
    # Calculate the date of the second Sunday
    second_sunday = first_day_of_month + datetime.timedelta(days=(6 - day_of_week + 7) % 7 + 7)
    return today == second_sunday


def create_showcase_sunday_megathread(reddit):
    subreddit = reddit.subreddit("developersIndia")
    title = "Showcase Sunday Megathread - {month} {year}".format(month=datetime.date.today().strftime("%B"), year=datetime.date.today().year)
    text = """
Welcome to the Showcase Sunday Megathread!
"""
    sticky = subreddit.submit(title, selftext=text, send_replies=False)
    sticky.mod.sticky(state=True, bottom=True)
    # sticky.mod.suggested_sort(sort='new')
    sticky.mod.flair(text="Megathread")
    return sticky.id

def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=user_agent
    )

    if is_second_sunday():
        create_showcase_sunday_megathread(reddit)

if __name__ == "__main__":
    main()