from connection import Connection

from googleapiclient.discovery import build

class GMail:
    def __init__(self, credentials):
        self.creds = credentials
        self.email_subjects = []
        self.from_email = []
        self.gmail = build('gmail', 'v1', credentials=self.creds)

    def get_emails(self, pageId=None):
        max_results = 25
        emails = self.gmail.users().messages().list(userId='me', maxResults=max_results, pageToken=pageId).execute()
        max_page_count = (emails['resultSizeEstimate'])
        nextPageToken = emails['nextPageToken']
        print(f'Getting page {self.page_count} of {max_page_count}')

        email_ids = [i['id'] for i in emails['messages']]
        
        for item in email_ids:
            res = self.gmail.users().messages().get(userId='me', id=item).execute()
            
            for header_value in res['payload']['headers']:
                
                if header_value['name'].lower() == 'subject':
                    self.email_subjects.append(header_value['value'])

                if header_value['name'].lower() == 'from':
                    self.from_email.append(header_value['value'])
                    
        if nextPageToken and self.page_count < 3:
            self.page_count += 1
            self.get_emails(pageId=nextPageToken)

        data = zip(self.from_email, self.email_subjects)

        # pprint.pprint(data)

        return data
        # values = [email for email in data]
        # body = {'values': values}

        # sheet_result = self.sheets.spreadsheets().values().update(
        #     spreadsheetId=self.spreadsheet_id,
        #     range=self.sheet_range,
        #     valueInputOption='USER_ENTERED',
        #     body=body
        # ).execute()
        # print(f'{sheet_result.get("updatedCells")} Cells updated.')
