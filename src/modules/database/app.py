from flask import Flask, render_template, request
import jinja2
import db_functions

app = Flask(__name__)

devicedataheadings = ("logid", "timestamp", "temperature", "humidity", "knockStatus", "deviceStatus")
userdataheadings = ("sessionId", "deviceId", "timestamp", "sessionDuration", "score")


@app.route('/')
def index():  # put application's code here

    devicedata = db_functions.get_devicedata()
    userdata = db_functions.get_userdata()

    return render_template('index.html', devicedataheadings=devicedataheadings, devicedata=devicedata,
                           userdataheadings=userdataheadings, userdata=userdata)


if __name__ == '__main__':
    app.run()

# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
