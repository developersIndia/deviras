import praw
from collections import defaultdict
import os
import json
import requests

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
user_agent = 'User Flair Usage'
sub = "developersIndia"

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=reddit_pass,
    user_agent=user_agent
)

# Select the subreddit
subreddit = reddit.subreddit(sub)

# Initialize a dictionary to count flairs
flair_count = defaultdict(int)

# Iterate over all the flairs
emoji_flair_count = 0
emoji_flair_users = []
for flair in subreddit.flair(limit=None):
    f = flair['flair_text'].strip()

    if f.startswith(":") or f.endswith(":"):
        emoji_flair_count += 1
        emoji_flair_users.append(
            dict(
                user=flair['user'],
                flair_text=f
            )
        )
    else:
        flair_count[flair['flair_text'].strip()] += 1

# Convert the dictionary to a list of tuples and sort it by the count
sorted_flairs = sorted(flair_count.items(), key=lambda x: x[1], reverse=True)

# Fetch the list of available user flairs
available_flairs = []
for flair in subreddit.flair.templates:
    if not flair['mod_only']:
        available_flairs.append(flair['text'].strip())


# Initialize a dictionary to count available flairs
available_flair_count = defaultdict(int)
old_available_flair_count = defaultdict(int)
# Iterate over the sorted flairs
for flair, count in sorted_flairs:
    # If the flair is available, increment its count
    if flair in available_flairs:
        available_flair_count[flair] += count
    else:
        old_available_flair_count[flair] += count


total_count = sum(available_flair_count.values())
old_flairs_total_count = sum(old_available_flair_count.values())

# print(f"Users with un-supported (old) text flairs: {old_flairs_total_count}")
# print(f"Users with supported text flairs: {total_count}")
# print(f"Users with emoji only flairs: {emoji_flair_count}")
# print(f"Total count of user-flairs: {total_count + emoji_flair_count + old_flairs_total_count}")

data = {
    'Users with custom text flairs': f"**{old_flairs_total_count}**",
    'Users with supported text flairs': f"**{total_count}**",
    'Users with emoji only flairs': f"**{emoji_flair_count}**",
    'Total count of user-flairs': f"**{total_count + emoji_flair_count + old_flairs_total_count}**"
}

formatted_data = "\n".join([f"{k}: {v}" for k, v in data.items()])  # Format the data as a string with each item on a new line

requests.post(webhook_url, json={"content": formatted_data})