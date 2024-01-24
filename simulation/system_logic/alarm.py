import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher


class Alarm:
    _system_active = False
    _alarm_active = False
    _reason = None
    _pin = "1234"
    _lock = threading.Lock()

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
    def get_pin(cls):
        with cls._lock:
            return cls._pin
