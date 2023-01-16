import odroid_wiringpi as wpi
import odroid_dht11 as dht11

wpi.wiringPiSetup()

# read data using pin 7
instance = dht11.DHT11(pin = 9)
result = instance.read()
print(result)
print(result.temperature)

if result.is_valid():
    print("Temperature: %-2d C" % result.temperature)
    print("Humidity: %-2d %%" % result.humidity)
else:
    print("Error: %d" % result.error_code)