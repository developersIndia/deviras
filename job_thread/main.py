import json
import logging
import re
from copy import deepcopy
from dataclasses import dataclass
from os import environ, fsync
from time import strftime, time

import feedparser
import praw

SECONDS_IN_WEEK = 60 * 60 * 24 * 7

# Date Month, Year
STRFTIME_FORMAT = "%d %B, %Y"

import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

class Config:
    DB_PATH = "db.json"
    SUBREDDIT = "developersindia"

    POST_FLAIR = "Hiring"
    POST_TITLE = f"Don't Miss Out on These Job Opportunities | Weekly Job Openings Thread | {strftime(STRFTIME_FORMAT)}"
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


@dataclass
class Post:
    post_id: str
    epoch: int


def dict_raise_or_set(d, key, value):
    if d.get(key) is not None:
        raise ValueError(f"Key {key} already present in dictionary")

    d[key] = value


class DB:
    POSTS = "postid_epoch"
    COMMENTS = "jobid_commentid"

    def __init__(self, db_path):
        try:
            self._fp = open(db_path, "r+")
            self._db = json.loads(self._fp.read() or "{}")
        except FileNotFoundError:
            self._fp = open(db_path, "w")
            self._db = {}

        self._copy = None

        self._create()

    def __enter__(self):
        self._copy = deepcopy(self._db)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # We re-write the DB on each transaction as we cannot guarantee "atomicity"
        # when dealing with external APIs. Eg, we can locally roll back a transaction
        # inserting multiple posts into the DB in case of an exception, but the
        # posts obviously won't be deleted on the reddit side. So we write
        # as much as possible incrementally to prevent losing track of already created
        # posts, preventing their re-creation server side in case of a crash.
        if exc_type:
            self._db = self._copy
        # If a change was actually made
        elif self._db != self._copy:
            self._fp.seek(0)
            self._fp.write(json.dumps(self._db, indent=4))
            self._fp.truncate()  # Trim the file to the desired size
            fsync(self._fp)

        self._copy = None

    def _create(self):
        with self:
            self._db.setdefault(DB.POSTS, {})
            self._db.setdefault(DB.COMMENTS, {})

    def get_latest_post(self) -> Post | None:
        # {"id": 1234, "id2": "5678"} -> ("id2", "5678") (Descending)
        try:
            result = sorted(
                self._db[DB.POSTS].items(),
                key=lambda item: item[1],
                reverse=True,
            )[0]
        except IndexError:
            return None

        return Post(post_id=result[0], epoch=result[1])

    def insert_post(self, post: Post):
        with self:
            dict_raise_or_set(self._db[DB.POSTS], post.post_id, post.epoch)

    def insert_comment(self, feed_job_id: str, comment_id: str):
        with self:
            dict_raise_or_set(self._db[DB.COMMENTS], feed_job_id, comment_id)

    def is_job_posted(self, feed_job_id: str):
        return self._db[DB.COMMENTS].get(feed_job_id) is not None


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


def strip_html(text):
    return re.sub("<[^<]+?>", "", text)


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
            summary=strip_html(entry["summary"]),
            permalink=entry["link"],
        )
        for entry in entries
    ]


def should_create_new_post(latest_post: Post) -> bool:
    if latest_post is not None:
        return (time() - latest_post.epoch) >= SECONDS_IN_WEEK

    return True


def create_job_post(subreddit) -> Post:
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
    submission.mod.distinguish()
    submission.mod.approve()

    return Post(post_id=submission.id, epoch=submission.created_utc)


def main():
    logging.root.setLevel(logging.INFO)

    db = DB(Config.DB_PATH)
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
            logging.info(f"Un-pinning old post {maybe_old_post}")

            try:
                reddit.submission(maybe_old_post.post_id).mod.sticky(
                    state=False
                )
            except Exception:
                logging.warning(f"Failed to un-pin post!", exc_info=True)

        new_post = create_job_post(subreddit)

        logging.info(f"Created new post {new_post}")

        db.insert_post(new_post)

    submission = reddit.submission(db.get_latest_post().post_id)

    logging.info(f"Fetched latest submission {submission.id}")

    for job in get_job_entries(Config.FEED_URL):
        if db.is_job_posted(job.post_id):
            logging.warning(
                f"Ignoring already posted job with post ID {job.post_id}"
            )
            continue

        comment_text = f"""\
[**{job.title}** - {job.company_name}]({job.permalink})

**Salary:** {job.salary}

**Location:** {job.location}

**Job Type:** {job.job_type}

### Summary

{job.summary}\
"""

        comment = submission.reply(comment_text)
        db.insert_comment(job.post_id, comment.id)

        logging.info(
            f"Posted job with post ID {job.post_id} as reddit comment {comment.id}"
        )


if __name__ == "__main__":
    main()
