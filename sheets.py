import datetime
import os
from googleapiclient.discovery import build

from rich import print


class SpreadSheet:
    def __init__(self, credentials):
        self.creds = credentials
        self.sheets = build('sheets', 'v4', credentials=self.creds)
        self.sheet_range = 'Sheet1!A:C'
        self.spreadsheet_url = None

    def _open_sheet(self, sheet_id):
        '''Private method
           Opens an existing spreadsheet.
        '''
        ss_id = sheet_id

        print("Spreadsheet Found")
        self.spreadsheet_id = ss_id
        sheet = self.sheets.spreadsheets()
        self.spreadsheet_url = sheet.get(spreadsheetId=ss_id).execute()
        result = sheet.values().get(spreadsheetId=ss_id, range=self.sheet_range).execute()
        values = result.get('values', [])
        if not values:
            print('Sheet Empty')
            return

        print('From\tSubject')
        for row in values:
            # if 'no-reply' in row[0].lower():
            #     pass
            # elif 'noreply' in row[0].lower():
            #     pass
            # else:
            #     print(f'{row[0]}{row[1]}')
            print(f'{row[0]}{row[1]}')

    def _create_sheet(self):
        '''Private method

            Creates a new spreadsheet.
        '''
        print("Creating new spreadsheet")
        requests = []
        # Set the spreadsheet's title.
        requests.append({
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': f"Emails - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                'fields': 'title'
            }
        })
        body = {
            "requests": requests
        }
        sheet = self.sheets.spreadsheets().create().execute()
        if sheet:
            self.spreadsheet_id = sheet['spreadsheetId']
            sheet = self.sheets.spreadsheets()
            self.spreadsheet_url = sheet.get(
                spreadsheetId=self.spreadsheet_id).execute()

            resp = self.sheets.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            print(dir(resp))
            with open('spreadsheet.id', 'w') as f:
                f.write(self.spreadsheet_id)

    def open_or_create_sheet(self):
        '''Decide weather or not to create a new sheet or open an existing sheet
           Nothing fancy going on here, basically if there's a spreadsheet.id file
           then open it and use that ID. Otherwise create a new file.
        '''
        if os.path.exists('spreadsheet.id'):
            with open('spreadsheet.id', 'r') as s_id:
                ss_id = s_id.read()
            self._open_sheet(ss_id)
        else:
            self._create_sheet()

    def add_emails_to_sheet(self, data):
        values = [email for email in data]
        body = {'values': values}

        sheet_result = self.sheets.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet_range,
            valueInputOption='USER_ENTERED',
            # insertDataOption='INSERT_ROWS', # Uncomment for appending.
            body=body
        ).execute()
        print(f'{sheet_result.get("updatedCells")} Cells updated.')

    def add_new_sheet(self, sheet_title):
        requests = []

        requests.append({
                "addSheet": {
                    "properties": {
                        "title": sheet_title,

                        "tabColor": {
                            "red": 1.0,
                            "green": 0.3,
                            "blue": 0.4
                        }
                    }
                }
            })

        body = {
            'requests': requests,
        }

        resp = self.sheets.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()
        print(dir(resp))
