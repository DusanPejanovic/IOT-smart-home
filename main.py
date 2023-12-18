import threading

from controllers.msw_controller import MSWController
from controllers.uds_controller import UDSController
from settings import load_settings
from controllers.dht_controller import DHTController
from controllers.btn_controller import ButtonController
from controllers.pir_controller import PirController

import time

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


class SmartHomeController:
    def __init__(self):
        self.threads = []
        self.console_lock = threading.Lock()
        self.stop_event = threading.Event()

    def run_controller(self, pi_id, component_id, settings):
        component_type = settings["type"]
        if component_type == "PIR":
            pir_controller = PirController(pi_id, component_id, settings, self.threads, self.console_lock,
                                                 self.stop_event)
            pir_controller.run_loop()
        elif component_type == "UDS":
            uds_controller = UDSController(pi_id, component_id, settings, self.threads, self.console_lock,
                                                 self.stop_event)
            uds_controller .run_loop()
        elif component_type == "BTN":
            button_controller = ButtonController(pi_id, component_id, settings, self.threads, self.console_lock,
                                                 self.stop_event)
            button_controller.run_loop()
        elif component_type == "DHT":
            dht_controller = DHTController(pi_id, component_id, settings, self.threads, self.console_lock,
                                           self.stop_event)
            dht_controller.run_loop()
        elif component_type == "MSW":
            msw_controller = MSWController(pi_id, component_id, settings, self.threads, self.console_lock,
                                           self.stop_event)
            msw_controller.run_loop()

    def stop(self):
        self.stop_event.set()


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    smart_home = SmartHomeController()
    try:
        for pi_id, pi_settings in settings.items():
            for component_id, component_settings in pi_settings.items():
                smart_home.run_controller(pi_id, component_id, component_settings)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping app')
        smart_home.stop()
