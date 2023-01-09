import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []
portAddress = []

for onePort in ports:
    portList.append(str(onePort))
    port = (str(onePort))
    split_port = port.split(" ", 1)
    substring = split_port[0]
    portAddress.append(substring)

for address in portAddress:
    
 arduino = serial.Serial(address, 115200, timeout=.1)

 while True:
     data = arduino.readline()[:-2]
     if data:
         print(data)

