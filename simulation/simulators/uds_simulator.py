import time
import random
import threading


class UDSSimulator:
    def __init__(self, callback, stop_event):
        self.callback = callback
        self.stop_event = stop_event

    def simulate_distance(self):
        while not self.stop_event.is_set():
            time.sleep(random.uniform(1, 5))
            distance = random.uniform(100, 1000)
            self.callback(distance)

    def start(self):
        thread = threading.Thread(target=self.simulate_distance)
        thread.start()
        return thread
