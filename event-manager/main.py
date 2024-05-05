import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')
guild_id = int(os.getenv('DISCORD_GUILD_ID'))
calendar_id = os.getenv('GOOGLE_CALENDAR_ID')

def get_input():
    NAME = input("Event title: ")
    DESCRIPTION = input("Event description: ")
    LOCATION = input("Event location (red -> for developersindia subreddit): ")
    if LOCATION == "red":
        LOCATION = "https://www.reddit.com/r/developersindia/"
    DATE = input("Enter the event date (yyyy-mm-dd): ")
    START_TIME = input("Enter the event start time (hh:mm)- ")
    END_TIME = input("Enter the event end time (hh:mm)- ")

    return NAME, DESCRIPTION, LOCATION, DATE, START_TIME, END_TIME

EVENT_NAME, EVENT_DESCRIPTION, EVENT_LOCATION, EVENT_DATE, EVENT_START_TIME, EVENT_END_TIME = get_input()

# Execute create_discord_event
from discord_bot import create_discord_event
create_discord_event(bot_token, guild_id, EVENT_NAME, EVENT_DESCRIPTION, EVENT_LOCATION, EVENT_DATE, EVENT_START_TIME, EVENT_END_TIME)

# Execute google_calendar_event
from google_calendar import create_google_calendar_event
create_google_calendar_event(calendar_id, EVENT_NAME, EVENT_DESCRIPTION, EVENT_LOCATION, EVENT_DATE, EVENT_START_TIME, EVENT_END_TIME)