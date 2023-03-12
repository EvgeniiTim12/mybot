from __future__ import print_function
import sqlite3
import config
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
sql.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,refer_id INTEGER,user_id INTEGER,date TEXT,refer_card TEXT,idfor TEXT) ")
sql.execute("CREATE TABLE IF NOT EXISTS langue(id INTEGER,lang TEXT) ")
sql.execute("CREATE TABLE IF NOT EXISTS admins(id INTEGER,name TEXT) ")

def add_user(user_id,datime,refer_id=None):
    with sql.connection as con:
        if(refer_id!=None):
            con.execute("INSERT INTO users (user_id,refer_id,date,idfor) VALUES (?,?,?,?)",(user_id,refer_id,datime,user_id,))
        else:
            con.execute("INSERT INTO users (user_id,date,idfor) VALUES (?,?,?)",(user_id,datime,user_id,))

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

def update_card(user_id,card):
    with sql.connection as con:
        con.execute(f"UPDATE users SET refer_card='{card}' WHERE user_id={user_id}")

def get_card(user_id):
    with sql.connection as con:
        result = con.execute(f"SELECT refer_card FROM 'users' WHERE user_id = {user_id}").fetchone()[0]
        if result is None:
            return "None"
        else:
            return result


async def last_table():
    with sql.connection as con:
        con.execute("DROP TABLE IF EXISTS new_table")
        con.execute("CREATE TABLE IF NOT EXISTS new_table(id INTEGER PRIMARY KEY,kto_3aregal TEXT,kogo_3aregal TEXT,koli_3aregal TEXT,refer_card TEXT,idfor TEXT) ")
        i=0
        max=con.execute("SELECT MAX(id) FROM users").fetchone()[0]
        while(i<=max):
            try:
                name = con.execute(f"SELECT user_id FROM 'users' WHERE id = {i}").fetchone()[0]
                name_refer = con.execute(f"SELECT refer_id FROM 'users' WHERE id = {i}").fetchone()[0]
                date=con.execute(f"SELECT date FROM 'users' WHERE id = {i}").fetchone()[0]
                card=con.execute(f"SELECT refer_card FROM 'users' WHERE id = {i}").fetchone()[0]
                idfor=con.execute(f"SELECT idfor FROM 'users' WHERE id = {i}").fetchone()[0]
                con.execute("INSERT INTO new_table (kogo_3aregal,kto_3aregal,koli_3aregal,refer_card,idfor) VALUES (?,?,?,?,?)",
                (str(await get_userbyid(name)),str(await get_userbyid(name_refer)),str(date),str(card),str(idfor),))
            except TypeError:
                pass
            i+=1
#########################################
class GoogleSheet:
    SPREADSHEET_ID = config.SPREADSHEET_ID
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
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        #print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

        
def mama():
    gs = GoogleSheet()
    test_range = 'testlist!A1:E'
    test_values = []
    startlist=["kto_3aregal","kogo_3aregal","koli_3aregal","card_number","delete id"]
    test_values.append(startlist)
    with sql.connection as con:
        i=0
        max=con.execute("SELECT MAX(id) FROM new_table").fetchone()[0]
        while(i<=max):
            try:
                name = con.execute(f"SELECT kto_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                name_refer = con.execute(f"SELECT kogo_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                date=con.execute(f"SELECT koli_3aregal FROM 'new_table' WHERE id = {i}").fetchone()[0]
                card=con.execute(f"SELECT refer_card FROM 'new_table' WHERE id = {i}").fetchone()[0]
                idfor=con.execute(f"SELECT idfor FROM 'new_table' WHERE id = {i}").fetchone()[0]
                if(card is None):
                    card="None"
                values=[name,name_refer,date,str(card),idfor]
                test_values.append(values)
            except TypeError:
                pass
            i+=1 
    endlist=["END","OF","TABLE",'.']
    test_values.append(endlist)
    for i in range(3):
        endlist=["","",""]
        test_values.append(endlist)
    
    gs.updateRangeValues(test_range, test_values)

   
#############
async def add_admin(user_id):
    with sql.connection as con:
        con.execute("INSERT INTO 'admins' VALUES (?,?)", (user_id,str(await get_userbyid(user_id))))

def check_admin(user_id):
    with sql.connection as con:
        result = con.execute(f"SELECT id FROM 'admins' WHERE id = {user_id}")
        return bool(len(result.fetchall()))

def remove_admin(user_id):
    with sql.connection as con:
        con.execute(f"DELETE FROM admins WHERE id={user_id}")

def remove_user(user_id):
    with sql.connection as con:
        try:
            con.execute(f"DELETE FROM users WHERE user_id={user_id}")
            return True
        except:
            return False


def close():
    connection.close()