import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_google_calendar_event(calendar_id, name, description, location, date, start_time, end_time):

    creds = None

    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Login to your Google account. [THIS IS A ONE TIME PROCESS]")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try :
        service = build('calendar', 'v3', credentials=creds)
        start = f"{date}T{start_time}:00"
        end = f"{date}T{end_time}:00"
        event = {
            'summary': name,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
             'dateTime': end,
            'timeZone': 'Asia/Kolkata',
            },
        }
        
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
        print('Google calendar: %s' % (event.get('htmlLink')))
        return event
    
    except Exception as e:
        print(e)
        return None
                                                                                                                                                                                                                                                                                                                         
# END