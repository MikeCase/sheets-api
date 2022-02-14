import os

import asyncio
from aiogoogle import Aiogoogle
from rich import print



class GMail:
    def __init__(self, credentials):
        self.creds = credentials
        self.email_subjects = []
        self.from_email = []
        self.page_count = 1
        

    async def get_emails(self, pageId=None, maxPageCount=3, max_results=25):
        '''Just get emails till you run out of nextPageTokens :P
           Ok not quite that extreme. I've set limits for the amount 
           of emails to return.
        '''
        async with Aiogoogle(service_account_creds=self.creds) as aiogoogle:
            gmail = await aiogoogle.discover('gmail', 'v1')
            res = await aiogoogle.as_service_account(
                gmail.users.messages.list(userId='me'),
            )
        print(res)
        # Get a list of emails from the server. 
        # the maximum amount of results returned is
        # determined by max_results
    #     total_messages = self.gmail.users().getProfile(userId='me').execute()

    #     emails = self.gmail.users().messages().list(userId='me', maxResults=max_results, pageToken=pageId).execute()
    #     max_page_count = maxPageCount
    #     totalPages = total_messages['messagesTotal']/max_results
    #     nextPageToken = emails['nextPageToken']

    #     print(f'Getting page {self.page_count} of {totalPages}')

    #     email_ids = [e_id['id'] for e_id in emails['messages']]
        
    #     # Filter out everything except for from addresses and the subject. 
    #     for email_id in email_ids:
    #         res = self.gmail.users().messages().get(userId='me', id=email_id).execute()
            
    #         for header_value in res['payload']['headers']:
                
    #             if header_value['name'].lower() == 'subject':
    #                 self.email_subjects.append(header_value['value'])

    #             if header_value['name'].lower() == 'from':
    #                 self.from_email.append(header_value['value'])

    #     # If there's a next page token, then use that to read the next 
    #     # max_results batch. I think this is called recursion...             
    #     if nextPageToken and self.page_count < max_page_count:
    #         self.page_count += 1
    #         self.get_emails(pageId=nextPageToken, max_results=max_results)

    #     data = zip(self.from_email, self.email_subjects) # Combine the emails and the subject lines into one list. 


    #     return data
        

    # def _write_nextpage_token(self, npToken):
    #     with open('nptoken.tok', 'w', encoding='utf-8') as tkfile:
    #         tkfile.write(npToken)

    # def _read_nextpage_token(self, nptkFile):
    #     with open(nptkFile, 'r') as tkfile:
    #         return tkfile.readline()