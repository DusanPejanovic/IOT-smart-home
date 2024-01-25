import time
import random


def simulate_button_press(callback, stop_event):
    while not stop_event.is_set():
        # Simulate button press
        time.sleep(random.uniform(2, 5))
        callback(True)

        # Simulate button release
        time.sleep(random.uniform(2, 3))
        callback(False)
