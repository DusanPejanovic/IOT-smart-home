import time
import random


def simulate_rgb_diode(delay, callback, stop_event):
    colors = ['red', 'green', 'blue', 'white', 'yellow']

    while not stop_event.is_set():
        time.sleep(delay)
        color_index = random.randint(0, len(colors) - 1)
        callback(colors[color_index])
