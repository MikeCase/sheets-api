from __future__ import print_function


from googleapiclient.errors import HttpError

from rich import print

from connection import Connection
from gmail import GMail
from sheets import SpreadSheet
# from tabulate import tabulate



SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 'https://mail.google.com', ]

conn = Connection(SCOPES)

class MySpreedsheet:
    def __init__(self):
        """Shows basic usage of the Google sheets API.
            
        """
        self.sheet = None
        self.creds = conn.make_connection()

        try:
            # Call the Calendar API
            self.sheets = SpreadSheet(self.creds)
            self.email = GMail(self.creds)

            self.sheets.open_or_create_sheet()
            
        except HttpError as error:
            print('An error occurred: %s' % error)

    def add_emails(self, data):
        self.sheets.add_emails_to_sheet(data)

    def get_emails(self):
        return self.email.get_emails(max_results=50)

if __name__ == '__main__':
    ss = MySpreedsheet()
    # print(dir(ss))
    print('grabbing emails.. ')
    data = ss.get_emails()
    ss.add_emails(data)
    print(ss.sheets.spreadsheet_id)
    print(ss.sheets.spreadsheet_url['spreadsheetUrl'])