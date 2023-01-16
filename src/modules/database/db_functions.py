from db_connection import db
import mysql.connector
from mysql.connector import RefreshOption
import time

refresh = RefreshOption.LOG | RefreshOption.THREADS
cur = db.cursor()


def timestamp():
    ts = time.time()
    return ts

def insert_into_devicedata(dData):
    db.cmd_refresh()
    sql = "INSERT INTO devicedata (logid, timestamp, temperature, humidity, knockStatus, deviceStatus) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, dData)
    db.commit()


def insert_into_userdata(uData):
    db.cmd_refresh()
    sql = "INSERT INTO userdata (sessionId, deviceId, timestamp, sessionDuration, score) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, uData)
    db.commit()


def get_userdata():
    db.cmd_refresh(refresh)
    cur.execute("SELECT * FROM userdata")
    result = cur.fetchall()
    return result


def get_devicedata():
    db.cmd_refresh(refresh)
    cur.execute("SELECT * FROM devicedata")
    result = cur.fetchall()
    return result
