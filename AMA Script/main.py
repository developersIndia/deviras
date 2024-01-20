import praw
from dotenv import dotenv_values

# Load credentials from .env file
env_config = dotenv_values('.env')

# Reddit API credentials
client_id = env_config['REDDIT_CLIENT_ID']
client_secret = env_config['REDDIT_CLIENT_SECRET']
user_agent = env_config['REDDIT_USER_AGENT']
username = env_config['REDDIT_USERNAME']
password = env_config['REDDIT_PASSWORD']

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

post_url = 'https://reddit.com/r/developersIndia/' # replace with AMA post URL

submission = reddit.submission(url=post_url)
submission.comments.replace_more(limit=None)

guest_username = 'AMA_GUEST_USERNAME' # replace with AMA guest name
markdown_file = ''
question_number = 1

for comment in submission.comments.list():
    if comment.author and comment.author.name.lower() == guest_username.lower():
        question_text = comment.parent().body.replace('\n', ' ')
        question_link = 'https://reddit.com' + comment.parent().permalink
        markdown_file += f'{question_number}. [{question_text}]({question_link})\n'
        question_number += 1

# UWU

# UTF-8 encoding
with open('questions.md', 'w', encoding='utf-8') as file:
    file.write(markdown_file)

print('Markdown file generated successfully.')

