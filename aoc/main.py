import praw
import requests
import os

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = 'AdventOfCode Leaderboard Updater (by https://github.com/ni5arga/)'
aoc_session_cookie = os.environ["AOC_SESSION_COOKIE"]
aoc_leaderboard_code = os.environ["AOC_LEADERBOARD_CODE"]

aoc_url = f'https://adventofcode.com/{{year}}/leaderboard/private/view/{aoc_leaderboard_code}'

def get_leaderboard_data():
    response = requests.get(aoc_url.format(year=2023), cookies={'session': aoc_session_cookie})
    data = response.json()
    return data

def format_leaderboard(data):
    leaderboard_stats = "r/DevelopersIndia Advent of Code Leaderboard Stats\n\n"

    # Sort members by stars in descending order
    sorted_members = sorted(data['members'].values(), key=lambda x: x['stars'], reverse=True)

    # Include only the top 10 players
    for i, member_data in enumerate(sorted_members[:10]):
        leaderboard_stats += f"{i + 1}. {member_data['name']} - Stars: {member_data['stars']} | Score: {member_data['local_score']}\n"

    leaderboard_stats += f"\n[Advent of Code Leaderboard](https://adventofcode.com/2023/leaderboard/private/view/{aoc_leaderboard_code})\n"

    return leaderboard_stats

def update_reddit_post(reddit, post_id, new_stats):
    post = reddit.submission(id=post_id)
    post.edit(new_stats)

def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=user_agent
    )

    post_id = 'YOUR_REDDIT_POST_ID'

    if post_id == 'YOUR_REDDIT_POST_ID':
        post = reddit.subreddit('developersindia').submit('Advent of Code Leaderboard', selftext='devsindia')
        post_id = post.id

    leaderboard_data = get_leaderboard_data()

    formatted_stats = format_leaderboard(leaderboard_data)

    update_reddit_post(reddit, post_id, formatted_stats)

if __name__ == "__main__":
    main()
