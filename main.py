from __future__ import print_function

import os
import datetime
import os.path
import pprint
import sys
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://mail.google.com', ]
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

class MySpreedsheet:
    def __init__(self):
        """Shows basic usage of the Google sheets API.
            
        """
        self.sheet = None
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            # Call the Calendar API
            self.sheets = build('sheets', 'v4', credentials=self.creds)
            self.email = build('gmail', 'v1', credentials=self.creds)
            

        except HttpError as error:
            print('An error occurred: %s' % error)

    def create_new_sheet(self):
        self.sheet = self.sheets.spreadsheets().create().execute()
        if self.sheet:
            self.spreadsheet_id = self.sheet['spreadsheetId']
        print(self.sheet.keys())

    def list_emails(self):
        emails = self.email.users().messages().list(userId='me').execute()
        email_ids = [i['id'] for i in emails['messages']]
        for item in email_ids:
            res = self.email.users().messages().get(userId='me', id=item).execute()
            for sub in res['payload']['headers']:
                if sub['name'] == 'Subject':
                    print(sub['value'])


if __name__ == '__main__':
    ss = MySpreedsheet()
    ss.list_emails()