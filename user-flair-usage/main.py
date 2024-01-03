import praw
from collections import defaultdict
import os

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
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
for flair in subreddit.flair(limit=None):
    flair_count[flair['flair_text']] += 1

# Convert the dictionary to a list of tuples and sort it by the count
sorted_flairs = sorted(flair_count.items(), key=lambda x: x[1], reverse=True)

# Print the sorted list of flairs and their counts
for flair, count in sorted_flairs:
    print(f"Flair: {flair}, Count: {count}")

# Calculate and print the total count of all flairs
total_count = sum(flair_count.values())
print(f"Total count of all flairs: {total_count}")