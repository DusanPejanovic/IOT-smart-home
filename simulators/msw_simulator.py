import time
import random
import threading

# MembraneSwitch simulator class
class MembraneSwitchSimulator:
    def __init__(self, callback, stop_event):
        self.callback = callback
        self.stop_event = stop_event

    def simulate_interaction(self):
        while not self.stop_event.is_set():
            time.sleep(random.uniform(0.5, 5))
            self.callback()

    def start(self):
        thread = threading.Thread(target=self.simulate_interaction)
        thread.start()
        return thread

    def stop(self):
        self.stop_event.set()
