import logging
import sqlite3
from dataclasses import dataclass
from os import environ
from time import time

import feedparser
import praw

SECONDS_IN_WEEK = 60 * 60 * 24 * 7


class Config:
    DB_PATH = "posts.db"
    SUBREDDIT = "developersindia"

    POST_FLAIR = "Hiring"
    POST_TITLE = "Don't Miss Out on These Job Opportunities | Weekly Job Openings Thread"
    POST_TEXT = """\
This thread has all the latest job openings that haven't been posted on previous weekly threads.

If you have a job opening that you'd like to share with the community, you can post it using this link:- https://developersindia.in/post-a-job/

For all the available job openings, check out the Job Board at:- https://developersindia.in/job-board/

Stay tuned for updates on the latest job openings, and apply for the ones that interest you. Wishing you the best of luck in your job search!\
"""

    CLIENT_ID = environ["REDDIT_CLIENT_ID"]
    CLIENT_SECRET = environ["REDDIT_CLIENT_SECRET"]
    REDDIT_PASSWORD = environ["REDDIT_PASSWORD"]
    USERNAME = environ["REDDIT_USERNAME"]
    USER_AGENT = f"u/{USERNAME} Job Board"
    FEED_URL = "https://developersindia.in/?feed=job_feed"


class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        self.cur = self.conn.cursor()

        self._create()

    def _create(self):
        with self.conn:
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS Posts"
                "(post_id TEXT PRIMARY KEY, time INTEGER NOT NULL DEFAULT(UNIXEPOCH()))"
            )

    def get_latest_post(self):
        self.cur.execute("SELECT post_id, time from Posts ORDER BY time DESC")

        if (result := self.cur.fetchone()) is not None:
            return dict(result)

    def insert_post(self, post_id: str, timestamp: int):
        with self.conn:
            self.cur.execute(
                "INSERT INTO Posts (post_id, time) VALUES ((?), (?))",
                (post_id, timestamp),
            )


@dataclass
class Job:
    post_id: str  # Used for deduplication
    title: str
    company_name: str
    location: str
    job_type: str
    salary: str
    summary: str
    permalink: str


def get_job_entries(feed_url):
    entries = feedparser.parse(feed_url).entries

    return [
        Job(
            post_id=entry["post-id"],
            title=entry["title"],
            company_name=entry["job_listing_company"],
            location=entry.get("job_listing_location", "N/A"),
            job_type=entry["job_listing_job_type"],
            salary=entry.get("job_listing_salary", "N/A"),
            summary=entry["summary"],
            permalink=entry["link"],
        )
        for entry in entries
    ]


def should_create_new_post(latest_post):
    if latest_post is not None:
        return (time() - latest_post["time"]) >= SECONDS_IN_WEEK

    return True


def create_job_post(subreddit):
    # https://old.reddit.com/r/redditdev/comments/ovte4q/praw_flair_a_post/h7doqmd/?context=3
    flair = next(
        filter(
            lambda flair: flair["flair_text"] == Config.POST_FLAIR,
            subreddit.flair.link_templates.user_selectable(),
        )
    )

    submission = subreddit.submit(
        Config.POST_TITLE,
        selftext=Config.POST_TEXT,
        flair_id=flair["flair_template_id"],
    )
    submission.mod.sticky()

    return submission


def main():
    logging.root.setLevel(logging.INFO)

    db = Database(Config.DB_PATH)
    reddit = praw.Reddit(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        password=Config.REDDIT_PASSWORD,
        user_agent=Config.USER_AGENT,
        username=Config.USERNAME,
    )

    subreddit = reddit.subreddit(Config.SUBREDDIT)

    maybe_old_post = db.get_latest_post()

    logging.info(f"Latest post in database {maybe_old_post}")

    if should_create_new_post(maybe_old_post):
        # Un-stick/pin the old post
        if maybe_old_post is not None:
            logging.info(f"Un-pinning old post")

            try:
                reddit.submission(maybe_old_post["post_id"]).mod.sticky(
                    state=False
                )
            except Exception:
                logging.warning(f"Failed to un-pin post!", exc_info=True)

        new_submission = create_job_post(subreddit)

        logging.info(
            f"Created new post {new_submission.id} at {new_submission.created_utc}"
        )

        db.insert_post(new_submission.id, new_submission.created_utc)

    submission = reddit.submission(db.get_latest_post()["post_id"])

    logging.info(f"Fetched latest submission {submission.id}")


if __name__ == "__main__":
    main()
