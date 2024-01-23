import time
from datetime import datetime


def simulate_four_segment_display(delay, callback, stop_event):
    while not stop_event.is_set():
        time.sleep(delay)

        now = datetime.now()
        hours = now.hour
        minutes = now.minute

        first_digit = hours // 10
        second_digit = hours % 10
        third_digit = minutes // 10
        fourth_digit = minutes % 10

        callback([first_digit, second_digit, third_digit, fourth_digit])
