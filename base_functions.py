import sqlite3
from datetime import datetime, timedelta

from db import GetConnection


def CreateTableIfNotExist():
    conn=GetConnection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS weather (
                        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        pincode INt NOT NULL,
                        temperature FLOAT NOT NULL,
                        humidity INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS posted_user_map (
                        post_id INTEGER NOT NULL ,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(post_id) REFERENCES weather (post_id),
                        FOREIGN KEY(user_id) REFERENCES users (user_id)) 
                      """)

    conn.commit()
    conn.close()

def NumberOfDays(utctime)->float:
    stored_timestamp_str =utctime
    stored_time = datetime.strptime(stored_timestamp_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()
    time_diff = now - stored_time
    return time_diff.total_seconds()/86400
