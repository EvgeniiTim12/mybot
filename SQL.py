import sqlite3
import random
import string
import datetime
from main import get_userbyid


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

################################

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
        result=con.execute("SELECT COUNT(id) as count FROM users").fetchone()[0]+1
        i=0
        while(i<result):
            try:
                name = con.execute(f"SELECT user_id FROM 'users' WHERE id = {i}").fetchone()[0]
                name_refer = con.execute(f"SELECT refer_id FROM 'users' WHERE id = {i}").fetchone()[0]
                date=con.execute(f"SELECT date FROM 'users' WHERE id = {i}").fetchone()[0]
                con.execute("INSERT INTO new_table (kogo_3aregal,kto_3aregal,koli_3aregal) VALUES (?,?,?)",
                (str(await get_userbyid(name)),str(await get_userbyid(name_refer)),str(date),))
            except TypeError as ex:
                max=con.execute("SELECT MAX(id) FROM users").fetchone()[0]
                while(i<max):
                    i+=1
                    print(i)
                    try:
                        name = con.execute(f"SELECT user_id FROM 'users' WHERE id = {i}").fetchone()[0]
                        name_refer = con.execute(f"SELECT refer_id FROM 'users' WHERE id = {i}").fetchone()[0]
                        date=con.execute(f"SELECT date FROM 'users' WHERE id = {i}").fetchone()[0]
                        con.execute("INSERT INTO new_table (kogo_3aregal,kto_3aregal,koli_3aregal) VALUES (?,?,?)",
                        (str(await get_userbyid(name)),str(await get_userbyid(name_refer)),str(date),))
                    except TypeError:
                        pass
            i+=1



            


def close():
    connection.close()
