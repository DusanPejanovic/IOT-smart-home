import time
import random


def simulate_humidity_and_temperature(callback, stop_event, initial_temp=25, initial_humidity=20):
    while not stop_event.is_set():
        time.sleep(random.uniform(1, 5))
        temperature = initial_temp + random.randint(-1, 1)
        humidity = initial_humidity + random.randint(-1, 1)
        if humidity < 0:
            humidity = 0
        if humidity > 100:
            humidity = 100
        callback(humidity, temperature)
