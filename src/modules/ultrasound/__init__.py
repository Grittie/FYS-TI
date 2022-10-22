import odroid_wiringpi as wpi
import time


def __pinSetupUltraSound(__trigPin: int, __echoPin: int):
    wpi.pinMode(__trigPin, wpi.GPIO.OUTPUT)
    wpi.pinMode(__echoPin, wpi.GPIO.INPUT)

def getDistance(trigPin: int, echoPin: int):

    __pinSetupUltraSound(trigPin, echoPin)

    wpi.digitalWrite(trigPin, wpi.HIGH)
    time.sleep(0.00001)
    wpi.digitalWrite(trigPin, wpi.LOW)
    while wpi.digitalRead(echoPin) == 0:
        start_time = time.time()
    while wpi.digitalRead(echoPin) == 1:
        bounceback_time = time.time()
    pulse_duration:int = bounceback_time - start_time
    distance = round(pulse_duration*17150, 2)

    return distance
