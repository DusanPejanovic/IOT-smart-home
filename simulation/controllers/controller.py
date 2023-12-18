import json
import threading
import time
import paho.mqtt.publish as publish

from simulation.broker_settings import HOSTNAME, PORT


class Controller:
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

    def __init__(self, pi_id, component_id, settings, threads, console_lock, stop_event):
        self.pi_id = pi_id
        self.component_id = component_id
        self.settings = settings
        self.console_lock = console_lock
        self.threads = threads
        self.stop_event = stop_event

    def get_basic_info(self):
        t = time.localtime()
        basic_info = "*" * 20 + "\n"
        basic_info += f"Pi id: {self.pi_id}\n"
        basic_info += f"Component_id: {self.component_id}\n"
        basic_info += f"Timestamp: {time.strftime('%H:%M:%S', t)}"
        return basic_info

    def process_and_batch_measurements(self, measurements):
        with self.counter_lock:
            for measurement in measurements:
                payload = {
                    "measurement": measurement[0],
                    "simulated": True,
                    "runs_on": "Pi1",
                    "name": "Dht",
                    "value": measurement[1]
                }
                self.data_batch.append((measurement[0], json.dumps(payload), 0, True))
                self.publish_data_counter += 1

        if self.publish_data_counter >= self.publish_data_limit:
            self.publish_event.set()

    def callback(self, *args):
        raise NotImplementedError("Subclasses must implement this method")

    def run_loop(self):
        raise NotImplementedError("Subclasses must implement this method")


publisher_thread = threading.Thread(target=Controller.publisher_task, args=())
publisher_thread.daemon = True
publisher_thread.start()
