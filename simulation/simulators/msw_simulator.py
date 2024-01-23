import random
import time


def simulate_membrane_switch(delay, callback, stop_event):
    values = ['0', '1', '2', '3', '4']

    while not stop_event.is_set():
        time.sleep(delay)
        pressed_key = random.choice(values)
        callback(pressed_key)
