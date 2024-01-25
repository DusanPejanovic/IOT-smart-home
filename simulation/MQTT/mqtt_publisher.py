import json
import threading
from datetime import datetime

from paho.mqtt import publish

from broker_settings import HOSTNAME, PORT


class MQTTPublisher:
    data_batch = []
    publish_data_counter = 0
    publish_data_limit = 5
    publish_event = threading.Event()
    counter_lock = threading.Lock()

    @classmethod
    def publisher_task(cls):
        while True:
            cls.publish_event.wait()
            with cls.counter_lock:
                local_data_batch = cls.data_batch.copy()
                cls.publish_data_counter = 0
                cls.data_batch.clear()
            publish.multiple(local_data_batch, hostname=HOSTNAME, port=PORT)
            # print(f'Published {cls.publish_data_limit} values')
            cls.publish_event.clear()

    @classmethod
    def process_and_batch_measurements(cls, pi_name, device_name, measurements, simulated):
        with cls.counter_lock:
            for measurement in measurements:
                payload = {
                    "measurement": measurement[0],
                    "simulated": simulated,
                    "runs_on": pi_name,
                    "name": device_name,
                    "value": measurement[1],
                    "new_sensor_value": True,
                    "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                cls.data_batch.append((measurement[0], json.dumps(payload), 0, False))
                cls.publish_data_counter += 1

            if cls.publish_data_counter >= cls.publish_data_limit:
                cls.publish_event.set()

    @classmethod
    def publish_alarm(cls, type, reason):
        payload = {
            "measurement": "Alarm",
            "type": type,
            "reason": reason,
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        publish.single("alarm", json.dumps(payload), hostname=HOSTNAME, port=PORT)

    @classmethod
    def publish_alarm_event(cls, status):
        payload = {"status": status}
        publish.single("alarm-status", json.dumps(payload), hostname=HOSTNAME, port=PORT)

    @classmethod
    def publish_clock_alarm_event(cls, status):
        payload = {"status": status}
        publish.single("clock-alarm-status", json.dumps(payload), hostname=HOSTNAME, port=PORT)
