import praw
import os
import re
import ruamel.yaml

sub_name = os.environ["SUBREDDIT_NAME"]
client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
reddit_pass = os.environ["REDDIT_PASSWORD"]
username = os.environ["REDDIT_USERNAME"]

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=f"Automod reader by u/{username}",
                     username=username,
                     password=reddit_pass)

# Get the subreddit object
subreddit = reddit.subreddit(sub_name)

for wikipage in subreddit.wiki:
    if wikipage == f"{sub_name}/config/automoderator":
        content = subreddit.wiki["config/automoderator"]
        break

if content is None:
    print("AutoModerator configuration page not found in the subreddit's wiki")
    exit(1)

# Read the AutoModerator configuration
automod_config = content.content_md

config_text = content.content_md
yaml_sections = re.split(r'(?m)^---\n', config_text)[1:]

rules = []

# Parse each YAML section to get the rules
for yaml_text in yaml_sections:
    rule = {}
    comment_pattern = r"^\s*#\s*(.*)$"
    comments = [
        match.group(1)
        for match in re.finditer(comment_pattern, yaml_text, re.MULTILINE)
    ]
    # Load the YAML data using ruamel.yaml
    yaml_data = ruamel.yaml.safe_load(yaml_text)

    if len(comments) > 0:
        rule[comments[0]] = yaml_data
        rules.append(rule)

for rule in rules:
    for key, value in rule.items():
        print("rule name: ", key)
