import time
import random
import threading


class PIRSimulator:
    def __init__(self, motion_callback, stop_event):
        self.motion_callback = motion_callback
        self.stop_event = stop_event

    def simulate_motion(self):
        while not self.stop_event.is_set():
            time.sleep(random.uniform(1, 5))
            self.motion_callback()

    def start(self):
        thread = threading.Thread(target=self.simulate_motion)
        thread.start()
        return thread

    def stop(self):
        self.stop_event.set()
