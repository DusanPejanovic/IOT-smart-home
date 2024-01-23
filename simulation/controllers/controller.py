import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher
from utility.registry import ControllerRegistry


class Controller:
    console_lock = threading.Lock()
    stop_event = threading.Event()

    def __init__(self, pi_id, component_id, settings, threads):
        self.pi_id = pi_id
        self.component_id = component_id
        self.settings = settings
        self.threads = threads

        # Pretty print
        ControllerRegistry.register(self)

    def get_basic_info(self):
        t = time.localtime()
        basic_info = "*" * 20 + "\n"
        basic_info += f"Pi id: {self.pi_id}\n"
        basic_info += f"Component_id: {self.component_id}\n"
        basic_info += f"Timestamp: {time.strftime('%H:%M:%S', t)}"
        return basic_info

    def publish_measurements(self, measurements):
        MQTTPublisher.process_and_batch_measurements(self.pi_id,
                                                     self.component_id,
                                                     measurements,
                                                     self.settings['simulated'])

    def callback(self, *args):
        raise NotImplementedError("Subclasses must implement this method")

    def run_loop(self):
        raise NotImplementedError("Subclasses must implement this method")
