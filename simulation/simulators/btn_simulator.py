import time
import random


def simulate_button_press(callback, stop_event):
    while not stop_event.is_set():
        # Simulate button press
        time.sleep(random.uniform(1, 5))
        callback(True)

        # Simulate button release
        time.sleep(random.uniform(0.5, 2))
        callback(False)
