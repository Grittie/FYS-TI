from flask import Flask, render_template, request
import jinja2
import db_functions

app = Flask(__name__)

devicedataheadings = ("logid", "timestamp", "temperature", "humidity", "knockStatus", "deviceStatus")
userdataheadings = ("sessionId", "deviceId", "timestamp", "sessionDuration", "score")

@app.route('/testbuttons', methods= ['GET'])
def testbuttons():
    # TODO add button test function
    if request.method == 'GET':
        print("testbuttons")

    return render_template('testbuttons.html')


@app.route('/testmatrix', methods= ['GET'])
def testmatrix():
    # TODO add matrix test function
    if request.method == 'GET':
        print('testing matrix')
    return render_template('testmatrix.html')


@app.route('/testmascottes', methods= ['GET'])
def testmascottes():
    # TODO add mascotte test function
    if request.method == 'GET':
        print('testing mascottes')
    return render_template('testmascottes.html')

@app.route('/db_dashboard', methods= ['GET'])
def index():  # put application's code here
    if request.method == 'GET':
        devicedata = db_functions.get_devicedata()
        userdata = db_functions.get_userdata()
    else:
        devicedata = db_functions.get_devicedata()
        userdata = db_functions.get_userdata()
    return render_template('db_dashboard.html', devicedataheadings=devicedataheadings, devicedata=devicedata,
                           userdataheadings=userdataheadings, userdata=userdata)


if __name__ == '__main__':
    app.run()

# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
