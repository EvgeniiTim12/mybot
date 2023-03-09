from __future__ import print_function
import sqlite3
import random
import string
import datetime
from main import get_userbyid

import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


connection=sqlite3.connect("server.db")
sql=connection.cursor()
print("connected")
sql.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,refer_id INTEGER,user_id INTEGER,date TEXT) ")
sql.execute("CREATE TABLE IF NOT EXISTS langue(id INTEGER,lang TEXT) ")

def add_user(user_id,refer_id=None):
    with sql.connection as con:
        if(refer_id!=None):
            con.execute("INSERT INTO users (user_id,refer_id,date) VALUES (?,?,?)",(user_id,refer_id,datetime.datetime.now(),))
        else:
            con.execute("INSERT INTO users (user_id,date) VALUES (?,?)",(user_id,datetime.datetime.now(),))

def check_reg(userid):
    with sql.connection as con:
        result=con.execute("SELECT user_id FROM users WHERE user_id = (?)",(userid,)).fetchall()
        return bool(len(result))

def get_refers(user_id):
    with sql.connection as con:
        result=con.execute("SELECT COUNT(id) as count FROM users WHERE refer_id = (?)",(user_id,)).fetchone()[0]
        return result

def add_lang(user_id):
    with sql.connection as con:
        con.execute("INSERT INTO 'langue' VALUES (?,?)", (user_id,'ukr'))

def check_lang(user_id):
    with sql.connection as con:
        result = con.execute(f"SELECT id FROM 'langue' WHERE id = {user_id}")
        return bool(len(result.fetchall()))


def get_lang(user_id):
    with sql.connection as con:
        result = con.execute(f"SELECT lang FROM 'langue' WHERE id = {user_id}").fetchone()[0]
        return result

def update_lang(user_id,new):
    with sql.connection as con:
        con.execute(f"UPDATE langue SET lang='{new}' WHERE id={user_id}")


async def last_table():
    with sql.connection as con:
        con.execute("DROP TABLE IF EXISTS new_table")
        con.execute("CREATE TABLE IF NOT EXISTS new_table(id INTEGER PRIMARY KEY,kto_3aregal TEXT,kogo_3aregal TEXT,koli_3aregal TEXT) ")
        i=0
        max=con.execute("SELECT MAX(id) FROM users").fetchone()[0]
        while(i<=max):
            try:
                name = con.execute(f"SELECT user_id FROM 'users' WHERE id = {i}").fetchone()[0]
                name_refer = con.execute(f"SELECT refer_id FROM 'users' WHERE id = {i}").fetchone()[0]
                date=con.execute(f"SELECT date FROM 'users' WHERE id = {i}").fetchone()[0]
                con.execute("INSERT INTO new_table (kogo_3aregal,kto_3aregal,koli_3aregal) VALUES (?,?,?)",
                (str(await get_userbyid(name)),str(await get_userbyid(name_refer)),str(date),))
            except TypeError:
                pass
            i+=1
#########################################
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
        #print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

        
def mama():
   gs = GoogleSheet()
   test_range = 'testlist!A1:D'
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
                values=[name,name_refer,date]
                test_values.append(values)
            except TypeError:
                pass
            i+=1 
   gs.updateRangeValues(test_range, test_values)

def close():
    connection.close()