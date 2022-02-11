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

from rich import print, console
from tabulate import tabulate



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
            self.email_subjects = []
            self.from_email = []
            self.sheet_range = 'Sheet1!A:C'
            self.spreadsheet_url = None

        except HttpError as error:
            print('An error occurred: %s' % error)

    def open_or_create_sheet(self):
        ss_id = None
        if os.path.exists('spreadsheet.id'):
            with open('spreadsheet.id', 'r') as s_id:
                ss_id = s_id.read()
        
        if ss_id:
            self.spreadsheet_id = ss_id
            self.sheet = self.sheets.spreadsheets()
            result = self.sheet.values().get(spreadsheetId=ss_id,range=self.sheet_range).execute()
            values = result.get('values', [])
            if not values:
                print('Sheet Empty')
                return

            print('From\tSubject')
            for row in values:
                print(f'{row[0]}\t{row[1]}')

        else:
            self.sheet = self.sheets.spreadsheets().create().execute()
            if self.sheet:
                self.spreadsheet_url = self.sheet['spreadsheetUrl']
                self.spreadsheet_id = self.sheet['spreadsheetId']
                with open('spreadsheet.id', 'w') as f:
                    f.write(self.spreadsheet_id)

            print(self.sheet.keys())

    def get_emails(self):
        emails = self.email.users().messages().list(userId='me').execute()
        email_ids = [i['id'] for i in emails['messages']]
        
        for item in email_ids:
            res = self.email.users().messages().get(userId='me', id=item).execute()
            
            for header_value in res['payload']['headers']:
                
                if header_value['name'] == 'Subject':
                    self.email_subjects.append(header_value['value'])
                    
                if header_value['name'] == 'From' or header_value['name'] == 'FROM' or header_value['name'] == 'from':
                    # print(f".{header_value['value']}")
                    self.from_email.append(header_value['value'])
                    

        data = zip(self.from_email, self.email_subjects)

        pprint.pprint(data)

        values = [
            email for email in data
            # [subject for subject in self.email_subjects]
        ]
        body = {
            'values': values,
        }

        sheet_result = self.sheets.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet_range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        print(f'{sheet_result.get("updatedCells")} Cells updated.')

if __name__ == '__main__':
    ss = MySpreedsheet()
    ss.open_or_create_sheet()
    print('grabbing emails.. ')
    ss.get_emails()
    print(ss.spreadsheet_id)