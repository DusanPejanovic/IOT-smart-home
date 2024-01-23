import time
from datetime import datetime


def simulate_lcd(delay, callback, stop_event):
    while not stop_event.is_set():
        time.sleep(delay)

        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute

        callback(f"Current time : {current_hour}:{current_minute}")
