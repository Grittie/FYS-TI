from db_connection import db
from mysql.connector import RefreshOption
import datetime

refresh = RefreshOption.LOG | RefreshOption.THREADS
cur = db.cursor()


def get_timestamp():
    ts = datetime.datetime.now()
    return ts


def insert_into_devicedata(logid, timestamp, temperature, humidity, knockStatus, deviceStatus):
    db.cmd_refresh(refresh)
    sql = "INSERT INTO `devicedata`(`logid`, `timestamp`, `temperature`, `humidity`, `knockStatus`, `deviceStatus`) VALUES (%s, %s, %s, %s,%s,%s)"
    values = (logid, timestamp, temperature, humidity, knockStatus, deviceStatus)
    cur.execute(sql, values)
    db.commit()

def insert_into_userdata(sessionid, deviceId, timestamp, sessionDuration, score):
    db.cmd_refresh(refresh)
    sql = "INSERT INTO userdata(sessionId, deviceId, timestamp, sessionDuration, score) VALUES (%s, %s, %s, %s, %s)"
    values = (sessionid, deviceId, timestamp, sessionDuration, score)
    cur.execute(sql, values)
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


def get_sessionid():
    db.cmd_refresh(refresh)
    cur.execute("SELECT MAX(sessionId) FROM userdata")
    result = cur.fetchall()
    return result


def get_logid():
    db.cmd_refresh(refresh)
    cur.execute("SELECT logid FROM devicedata GROUP BY logid HAVING count(*) = 1 ORDER BY logid desc LIMIT 1")
    result = cur.fetchall()
    return result
