import praw
import os
import json
import re
import ruamel.yaml
from io import StringIO

yaml = ruamel.yaml.YAML()
yaml.default_flow_style = False

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

def find_automod_wiki():
    for wikipage in subreddit.wiki:
        if wikipage == f"{sub_name}/config/automoderator":
            content = subreddit.wiki["config/automoderator"]
            break

    if content is None:
        print("AutoModerator configuration page not found in the subreddit's wiki")
        exit(1)

    return content

# Parse the AutoModerator configuration file
def get_automod_rules(content):
    # Split the content into sections
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
        yaml_data = yaml.load(yaml_text)

        if len(comments) > 0:
            rule[comments[0]] = yaml_data
            rules.append(rule)

    return rules

def formatted_announcement(announcements):
    announcement_block = ""
    announcement_block += f"""{announcements["filler_text"]}\n\n"""
    announcement_block += "## Recent Announcements\n\n"
    for announcement in announcements["announcements"]:
        announcement_block += f"- **[{announcement['title']}]({announcement['url']})**\n"

    return announcement_block

def update_automod_rule(rules, announcements):
    for rule in rules:
        for rulename, config in rule.items():
            if rulename == "New post comment":
                # print(config)
                config["comment"] = announcements
                # new_content = yaml.dump(config)
    stream = StringIO()
    yaml.dump(rules, stream)
    yaml_text = stream.getvalue()
    stream.close()
    print(yaml_text)
    # TODO: Update the wiki page with the new content
    # subreddit.wiki["config/automoderator"].edit(yaml_text, reason="Update automod comment")


def get_comment():
    with open('new_post_automod.yaml', 'r') as file:
        yaml_content = file.read()

    # Load the YAML content into a Python object
    yaml_object = yaml.load(yaml_content, ruamel.yaml.RoundTripLoader)
    return yaml_object

# read the announcements from announcements.json
def read_announcements():
    with open('announcement.json', 'r') as file:
        announcements = json.load(file)
    return announcements


content = find_automod_wiki()
announcement = read_announcements()
form_anno = formatted_announcement(announcement)

rules = get_automod_rules(content)
update_automod_rule(rules, form_anno)