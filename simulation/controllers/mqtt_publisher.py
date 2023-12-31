import json
import threading

from paho.mqtt import publish

from simulation.broker_settings import HOSTNAME, PORT


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
            print(f'Published {cls.publish_data_limit} values')
            cls.publish_event.clear()

    @classmethod
    def process_and_batch_measurements(cls, pi_name, device_name, measurements, simulated=False):
        with cls.counter_lock:
            for measurement in measurements:
                payload = {
                    "measurement": measurement[0],
                    "simulated": simulated,
                    "runs_on": pi_name,
                    "name": device_name,
                    "value": measurement[1]
                }
                cls.data_batch.append((measurement[0], json.dumps(payload), 0, True))
                cls.publish_data_counter += 1

        if cls.publish_data_counter >= cls.publish_data_limit:
            cls.publish_event.set()


publisher_thread = threading.Thread(target=MQTTPublisher.publisher_task, args=())
publisher_thread.daemon = True
publisher_thread.start()
