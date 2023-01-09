import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))


# arduino = serial.Serial('COM1', 115200, timeout=.1)

# while True:
#     data = arduino.readline()[:-2]
#     if data:
#         print data

