from __future__ import print_function
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from jinja2 import Template

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1qd_WVEBLxswoRVdTE0hFi2PzhBHIqJLb7D1ViVBFrFI'
SAMPLE_RANGE_NAME = 'Schedule!A2:I900'


def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_events():
    service = build('sheets', 'v4', credentials=get_credentials())

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return [Event(v) for v in values]


class Event:
    def __init__(self, values):
        print(values)
        self.regional_time = values[0]
        self.broadcaster = values[1]
        self.track = values[2]
        self.day = values[3]
        self.local_time = values[4]
        self.ui_block = values[5]
        self.class_identifiers = values[6]
        self.speaker = values[7]
        if len(values) > 8:
            self.topic = values[8]


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    events = get_events()
    template_file = os.path.join(os.path.dirname(__file__), 'templates.html')
    template = Template(open(template_file).read())
    with open('index.html', 'w') as html_file:
        html_file.write(template.render(events=events))

if __name__ == '__main__':
    main()
