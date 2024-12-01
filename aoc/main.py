import praw
import requests
import os

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]
user_agent = 'AdventOfCode Leaderboard Updater - developersIndia'
aoc_session_cookie = os.environ["AOC_SESSION_COOKIE"]
aoc_leaderboard_code = os.environ["AOC_LEADERBOARD_CODE"]
aoc_year = os.environ.get("AOC_YEAR")
reddit_post_id = os.environ.get("AOC_LEADERBOARD_REDDIT_POST_ID")

aoc_url = f'https://adventofcode.com/{aoc_year}/leaderboard/private/view/{aoc_leaderboard_code}.json'

def get_leaderboard_data():
    response = requests.get(aoc_url.format(year=aoc_year), cookies={'session': aoc_session_cookie})
    data = response.json()
    return data

def format_leaderboard(data, num_players=100):
    leaderboard_stats = f"r/developersIndia Advent of Code {aoc_year} - Leaderboard\n\n"
    leaderboard_stats += "| Rank | Player | Stars | Score |\n"
    leaderboard_stats += "|------|--------|-------|-------|\n"

    # Sort members by stars in descending order
    sorted_members = sorted(data['members'].values(), key=lambda x: x['local_score'], reverse=True)

    # Include only the top players
    for i, member_data in enumerate(sorted_members[:num_players]):
        # check for non-zero local_score
        if member_data['local_score'] > 0:
            leaderboard_stats += f"| {i + 1} | {member_data['name']} | {member_data['stars']} | {member_data['local_score']} |\n"

    leaderboard_stats += f"\nUpdated every 24 hours"

    return leaderboard_stats

def update_reddit_post(reddit, post_id, new_stats):
    post = reddit.submission(id=post_id)
    post.edit(new_stats)

def main():
    if not reddit_post_id:
        print("Please set the AOC_LEADERBOARD_REDDIT_POST_ID environment variable.")
        return

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=reddit_pass,
        user_agent=user_agent
    )

    leaderboard_data = get_leaderboard_data()
    formatted_stats = format_leaderboard(leaderboard_data)
    update_reddit_post(reddit, reddit_post_id, formatted_stats)

if __name__ == "__main__":
    main()
