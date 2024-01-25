import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher


class Alarm:
    _system_active = False
    _alarm_active = False
    _reason = None
    _pin = "1234"
    _lock = threading.Lock()
    _alarm_activation_listeners = []

    @classmethod
    def add_alarm_activation_listener(cls, listener):
        with cls._lock:
            cls._alarm_activation_listeners.append(listener)

    @classmethod
    def _notify_alarm_activation(cls):
        for listener in cls._alarm_activation_listeners:
            listener()

    @classmethod
    def activate_system(cls):
        if cls._system_active:
            return

        time.sleep(10)
        with cls._lock:
            cls._system_active = True

    @classmethod
    def deactivate_system(cls):
        if cls._system_active:
            return

        with cls._lock:
            cls._system_active = False

    @classmethod
    def system_activated(cls):
        with cls._lock:
            return cls._system_active

    @classmethod
    def activate_alarm(cls, reason):
        if cls._alarm_active:
            return

        with cls._lock:
            cls._alarm_active = True
            cls._reason = reason
            cls._notify_alarm_activation()
            MQTTPublisher.publish_alarm("Activated", reason)

    @classmethod
    def deactivate_alarm(cls):
        if not cls._alarm_active:
            return

        with cls._lock:
            cls._system_active = False
            cls._alarm_active = False
            cls._reason = None

    @classmethod
    def alarm_activated(cls):
        with cls._lock:
            return cls._alarm_active

    @classmethod
    def get_reason(cls):
        with cls._lock:
            return cls._reason

    @classmethod
    def get_pin(cls):
        with cls._lock:
            return cls._pin

    @classmethod
    def run_loop(cls, stop_event):
        while not stop_event.is_set():
            time.sleep(1)
            with cls._lock:
                if cls._alarm_active:
                    MQTTPublisher.publish_alarm_event("On")
                else:
                    MQTTPublisher.publish_alarm_event("Off")




