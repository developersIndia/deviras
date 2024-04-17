# To get the event details from the user

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

# END