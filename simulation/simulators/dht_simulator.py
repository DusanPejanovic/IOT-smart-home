import threading
import time
import random


class DHTSimulator:
    def __init__(self, callback, stop_event):
        self.callback = callback
        self.stop_event = stop_event
        self.initial_temp = 25
        self.initial_humidity = 20

    def simulate_humidity_and_temperature(self):
        while not self.stop_event.is_set():
            time.sleep(random.uniform(1, 5))
            temperature = self.initial_temp + random.randint(-1, 1)
            humidity = self.initial_humidity + random.randint(-1, 1)
            if humidity < 0:
                humidity = 0
            if humidity > 100:
                humidity = 100
            self.callback(humidity, temperature)

    def start(self):
        thread = threading.Thread(target=self.simulate_humidity_and_temperature)
        thread.start()
        return thread
