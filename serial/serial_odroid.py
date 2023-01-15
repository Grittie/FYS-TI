import serial.tools.list_ports
from threading import Thread
import time


ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []
portAddress = []
btnControllerAddress = ""
buttonStates = [0,0,0,0,0,0,0,0]

def identify(address):
    arduino = serial.Serial(address, 115200, timeout=.1)
    global buttonStates
    while True:
        data = arduino.readline()[:-2]
        if data:
            decode = data.decode("ascii")
            device_data = decode.split("_")
            device_name = ""
            if device_data[0] == "0x01":
                device_name = "button controller"
            elif device_data[0] == "0x02":
                device_name = "7 segment controller"
            print(device_data)
            if device_data[1] == "129":
                buttonStates[0] = 1
                buttonStates[7] = 1

            elif device_data[1] == "1":
                buttonStates[0] = 0
                buttonStates[7] = 0

            elif device_data[1] == "130":
                buttonStates[0] = 1
                buttonStates[6] = 1

            elif device_data[1] == "2":
                buttonStates[0] = 0
                buttonStates[6] = 0

            elif device_data[1] == "132":
                buttonStates[0] = 1
                buttonStates[5] = 1

            elif device_data[1] == "4":
                buttonStates[0] = 0
                buttonStates[5] = 0

            elif device_data[1] == "136":
                buttonStates[0] = 1
                buttonStates[4] = 1

            elif device_data[1] == "8":
                buttonStates[0] = 0
                buttonStates[4] = 0

            elif device_data[1] == "144":
                buttonStates[0] = 1
                buttonStates[3] = 1

            elif device_data[1] == "16":
                buttonStates[0] = 0
                buttonStates[3] = 0

            elif device_data[1] == "160":
                buttonStates[0] = 1
                buttonStates[2] = 1

            elif device_data[1] == "32":
                buttonStates[0] = 0
                buttonStates[2] = 0            

            elif device_data[1] == "192":
                buttonStates[0] = 1
                buttonStates[1] = 1

            elif device_data[1] == "64":
                buttonStates[0] = 0
                buttonStates[1] = 0

for onePort in ports:
    portList.append(str(onePort))
    port = (str(onePort))
    split_port = port.split(" ", 1)
    substring = split_port[0]
    portAddress.append(substring)

def checkforbuttonpress():
    while True:
        time.sleep(1)
        print(buttonStates)
        if (buttonStates[0] == 1) and (buttonStates[7] == 1):
            print("button 7 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[6] == 1):
            print("button 6 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[5] == 1):
            print("button 5 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[4] == 1):
            print("button 4 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[3] == 1):
            print("button 3 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[2] == 1):
            print("button 2 is pressed")
        elif (buttonStates[0] == 1) and (buttonStates[1] == 1):
            print("button 1 is pressed")
            
for address in portAddress:
    address = Thread(target=identify, args=[address])
    address.start()

threadcheckingforbuttonpress = Thread(target=checkforbuttonpress)
threadcheckingforbuttonpress.start()
