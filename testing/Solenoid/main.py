import odroid_wiringpi as wpi
import time

RELAY_PIN = 8

wpi.wiringPiSetup()
wpi.pinMode(RELAY_PIN, wpi.OUTPUT)


def do_loop():
    while True:
        print("aan")
        wpi.digitalWrite(RELAY_PIN, 1)
        time.sleep(1)
        print("uit")
        wpi.digitalWrite(RELAY_PIN, 0)
        time.sleep(1)


do_loop()
