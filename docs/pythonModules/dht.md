# dht

Deze module is speciaal gemaakt om de luchtvochtigheid en temperatuur te meten.
Het maakt gebruik van [odroid_c1_dht11](https://github.com/unims77/odroid_c1_dht11).
Deze library is volledig geschreven in python en is dus qua timing niet heel betrouwbaar.
Daardoor probeert de module meerdere keren om een `result` te krijgen tot het lukt.

```py
def getTemperature(pin: int):
    instance = dht11.DHT11(pin)

    while True:
        result = instance.read()

        if result.is_valid():
            return result.temperature
```

## Functies

- getTemperature(pin: int): Returnt een temperatuur (celcius) als een float.
- getHumidity(pin: int): Returnt een luchtvochtigheid percentage als een float.
