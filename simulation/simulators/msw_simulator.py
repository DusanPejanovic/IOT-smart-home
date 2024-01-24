import random
import time


def simulate_membrane_switch(delay, callback, stop_event):
    values = ['0', '1', '2', '3', '4']
    idx = 1

    while not stop_event.is_set():
        time.sleep(delay)
        # pressed_key = random.choice(values)
        callback(values[idx])
        idx += 1
        if idx >= len(values):
            idx = 0
