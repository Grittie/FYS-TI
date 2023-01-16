import serial.tools.list_ports
from threading import Thread
import time


ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []
portAddress = []
btnControllerAddress = ""
buttonStates = [0,0,0,0,0,0,0,0]
ledState = [0,0,0,0,0,0,0,0]

def identify(address):
    arduino = serial.Serial(address, 115200, timeout=.1)
    global buttonStates
    
    #arduino.write(encoded_led)
    
    while True:
        data = arduino.readline()[:-2]
        if data:
            print(data)
            #decode = data.decode("ascii")            
            # device_data = decode.split("_")
            # device_name = ""
            # if device_data[0] == "0x01":
            #     device_name = "button controller"
            # elif device_data[0] == "0x02":
            #     device_name = "7 segment controller"
            # print(device_data)
            # if device_data[1] == "129":
            #     buttonStates[0] = 1
            #     buttonStates[7] = 1
            #     arduino.write("7".encode())

            # if device_data[1] == "1":
            #     buttonStates[0] = 0
            #     buttonStates[7] = 0
            #     arduino.write("0".encode())

            # if device_data[1] == "130":
            #     buttonStates[0] = 1
            #     buttonStates[6] = 1
            #     arduino.write("6".encode())
            #     print("130".encode())

            # if device_data[1] == "2":
            #     buttonStates[0] = 0
            #     buttonStates[6] = 0
            #     arduino.write("0".encode())

            # if device_data[1] == "132":
            #     buttonStates[0] = 1
            #     buttonStates[5] = 1
            #     arduino.write("132\n".encode("ascii"))

            # if device_data[1] == "4":
            #     buttonStates[0] = 0
            #     buttonStates[5] = 0
            #     arduino.write("4\n".encode("ascii"))

            # if device_data[1] == "136":
            #     buttonStates[0] = 1
            #     buttonStates[4] = 1
            #     arduino.write("136\n".encode("ascii"))

            # if device_data[1] == "8":
            #     buttonStates[0] = 0
            #     buttonStates[4] = 0
            #     arduino.write("8\n".encode("ascii"))

            # if device_data[1] == "144":
            #     buttonStates[0] = 1
            #     buttonStates[3] = 1
            #     arduino.write("144\n".encode("ascii"))

            # if device_data[1] == "16":
            #     buttonStates[0] = 0
            #     buttonStates[3] = 0
            #     arduino.write("16\n".encode("ascii"))

            # if device_data[1] == "160":
            #     buttonStates[0] = 1
            #     buttonStates[2] = 1
            #     arduino.write("160\n".encode("ascii"))

            # if device_data[1] == "32":
            #     buttonStates[0] = 0
            #     buttonStates[2] = 0  
            #     arduino.write("32\n".encode("ascii"))          

            # if device_data[1] == "192":
            #     buttonStates[0] = 1
            #     buttonStates[1] = 1
            #     arduino.write("192\n".encode("ascii"))

            # if device_data[1] == "64":
            #     buttonStates[0] = 0
            #     buttonStates[1] = 0
            #     arduino.write("64\n".encode("ascii"))
        
        while True:
            if (ledState[0] == 1) and (ledState[7] == 1):
                arduino.write("129".encode("ascii"))
                print("Set led 7 on")
            if (ledState[0] == 0) and (ledState[7] == 0):
                arduino.write("1".encode("ascii"))
                print("Set led 7 off")
            if (ledState[0] == 1) and (ledState[6] == 1):
                arduino.write("130".encode("ascii"))
                print("Set LED 6 on")
            if (ledState[0] == 0) and (ledState[6] == 0):
                arduino.write("2".encode("ascii"))
                print("Set LED 6 off")
            time.sleep(1)

for onePort in ports:
    portList.append(str(onePort))
    port = (str(onePort))
    split_port = port.split(" ", 1)
    substring = split_port[0]
    portAddress.append(substring)

def checkforbuttonpress():
    while True:
        time.sleep(0.05)
        #print(buttonStates)
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


def cycleLed():
    while True:
        ledState[0] = 1
        ledState[1] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[1] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[2] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[2] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[3] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[3] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[4] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[4] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[5] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[5] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[6] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[6] = 0
        time.sleep(1)
        ledState[0] = 1
        ledState[7] = 1
        time.sleep(1)
        ledState[0] = 0
        ledState[7] = 0
        
for address in portAddress:
    address = Thread(target=identify, args=[address])
    address.start()

threadcheckingforbuttonpress = Thread(target=checkforbuttonpress)
threadcheckingforbuttonpress.start()
threadupdatingleds = Thread(target=cycleLed)
threadupdatingleds.start()
