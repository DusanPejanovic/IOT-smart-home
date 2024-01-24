import time
import random


def simulate_uds_distance(callback, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(3, 5))
        distance = random.uniform(100, 1000)
        callback(distance)
