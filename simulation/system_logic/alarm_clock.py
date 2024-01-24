import threading
import time
from datetime import datetime


class AlarmClock:
    _start_time = None
    _end_time = None
    _alarm_active = False
    _lock = threading.Lock()

    @classmethod
    def set_alarm(cls, start_time, end_time):
        with cls._lock:
            cls._start_time = start_time
            cls._end_time = end_time

    @classmethod
    def check_alarm(cls, stop_event):
        while not stop_event.is_set():
            time.sleep(1)
            current_time = datetime.now().time()
            with cls._lock:
                if cls._start_time is not None and cls._end_time is not None:
                    alarm_should_be_active = cls._start_time.time() <= current_time <= cls._end_time.time()
                    cls._alarm_active = alarm_should_be_active
                else:
                    cls._alarm_active = False

    @classmethod
    def is_alarm_active(cls):
        with cls._lock:
            return cls._alarm_active
