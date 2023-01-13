from db_connection import db
import time

cur = db.cursor()

def timestamp():
    ts = time.time()
    return ts

def insert_into_devicedata(dData):
    sql = "INSERT INTO devicedata (logid, timestamp, temperature, humidity, knockStatus, deviceStatus) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, dData)
    db.commit()


def insert_into_userdata(uData):
    sql = "INSERT INTO userdata (sessionId, deviceId, timestamp, sessionDuration, score) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, uData)
    db.commit()


def get_userdata():
    cur.execute("SELECT * FROM userdata")
    result = cur.fetchall()
    return result


def get_devicedata():
    cur.execute("SELECT * FROM devicedata")
    result = cur.fetchall()
    return result
