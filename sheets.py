from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import sqlite3

connection=sqlite3.connect("server.db")
sql=connection.cursor()
class GoogleSheet:
    SPREADSHEET_ID = '1wpawHPkTmqhccKS-440bS_DZHcjHX0ZIo0zfMWMI4Yk'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

        
def mama():
   gs = GoogleSheet()
   test_range = 'testlist!A1:D3'
   test_values = [
       
   ]
   with sql.connection as con:
        i=0
        max=con.execute("SELECT MAX(id) FROM new_table").fetchone()[0]
        while(i<=max):
            try:
                name = con.execute(f"SELECT kto_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                name_refer = con.execute(f"SELECT kogo_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                date=con.execute(f"SELECT koli_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                print(name,name_refer,date,"\n")
                values=[name,name_refer,date]
                test_values.append(values)
                print(test_values)
            except TypeError:
                pass
            i+=1 
   gs.updateRangeValues(test_range, test_values)


if __name__ == '__main__':
    mama()