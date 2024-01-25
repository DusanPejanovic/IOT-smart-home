import time
import random


def generate_value():
    commands = ["OK", "1", "2", "3"]
    return commands[random.randint(0, 3)]


def run_ir_receiver_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        time.sleep(delay)
        callback(generate_value())
