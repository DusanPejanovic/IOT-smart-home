import threading
import time
from datetime import datetime
from MQTT.mqtt_publisher import MQTTPublisher


class AlarmClock:
    _start_time = None
    _alarm_active = False
    _lock = threading.Lock()
    _alarm_clock_activation_listeners = []

    @classmethod
    def add_alarm_clock_activation_listener(cls, listener):
        with cls._lock:
            cls._alarm_clock_activation_listeners.append(listener)

    @classmethod
    def _notify_alarm_clock_activation(cls):
        for listener in cls._alarm_clock_activation_listeners:
            listener()

    @classmethod
    def set_alarm(cls, start_time):
        with cls._lock:
            cls._start_time = start_time

    @classmethod
    def turn_off(cls):
        with cls._lock:
            if not cls._alarm_active:
                return

            cls._start_time = None
            cls._alarm_active = False

    @classmethod
    def check_alarm(cls, stop_event):
        while not stop_event.is_set():
            time.sleep(1)
            current_time = datetime.now()
            with cls._lock:
                if cls._start_time is not None and current_time > cls._start_time and not cls._alarm_active:
                    cls._alarm_active = True

                if cls._alarm_active:
                    MQTTPublisher.publish_clock_alarm_event("On")
                else:
                    MQTTPublisher.publish_clock_alarm_event("Off")

    @classmethod
    def is_alarm_active(cls):
        with cls._lock:
            return cls._alarm_active
