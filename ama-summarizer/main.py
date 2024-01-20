import praw
import os
from dotenv import dotenv_values

def get_reddit_instance():
    # Reddit API credentials
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:109.0) Gecko/20100101 Firefox/121.0'
    client_id = os.environ["REDDIT_CLIENT_ID"]
    client_secret = os.environ["REDDIT_CLIENT_SECRET"]
    reddit_pass = os.environ["REDDIT_PASSWORD"]
    username = os.environ["REDDIT_USERNAME"]

    # Create a Reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=reddit_pass,
                         user_agent=user_agent,
                         username=username)
    return reddit


def get_post_url():

    post_url = input("Enter the AMA post URL: ") # reddit.com URLs preferred 
    return post_url

def get_guest_username():

    guest_username = input("Enter the AMA guest username: ") 
    return guest_username

def main():
    reddit = get_reddit_instance()
    
    post_url = get_post_url()
    guest_username = get_guest_username()

    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)

    markdown_file = ''
    question_number = 1

    for comment in submission.comments.list():
        if comment.author and comment.author.name.lower() == guest_username.lower():
            question_text = comment.parent().body.replace('\n', ' ')
            question_link = 'https://reddit.com' + comment.parent().permalink
            markdown_file += f'{question_number}. [{question_text}]({question_link})\n'
            question_number += 1

    # UTF-8 encoding
    with open('questions.md', 'w', encoding='utf-8') as file:
        file.write(markdown_file)

    print('Markdown file questions.md generated successfully.')

if __name__ == "__main__":
    main()


