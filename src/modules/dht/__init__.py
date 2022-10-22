import odroid_dht11 as dht11

def getTemperature(pin: int):
    instance = dht11.DHT11(pin)

    while True:
        result = instance.read()

        if result.is_valid():
            return result.temperature

def getHumidity(pin: int):
    instance = dht11.DHT11(pin)

    while True:
        result = instance.read()

        if result.is_valid():
            return result.humidity
