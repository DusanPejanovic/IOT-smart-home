import time
import random
import threading


def simulate_pir_motion(callback, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(3, 5))
        callback()
