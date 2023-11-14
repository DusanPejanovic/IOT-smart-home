import threading

from controllers.uds_controller import run_uds
from settings import load_settings
from controllers.dht_controller import run_dht
from controllers.btn_controller import run_button
from controllers.pir_controller import run_pir
from controllers.msw_controller import run_msw

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

    def run_controller(self, component_type, settings):
        print('Broj tredova: ' + str(len(self.threads)))
        if component_type == "PIR":
            run_pir(settings, self.threads, self.stop_event)
        elif component_type == "UDS":
            run_uds(settings, self.threads, self.stop_event)
        elif component_type == "BTN":
            run_button(settings, self.threads, self.stop_event)
        elif component_type == "DHT":
            run_dht(settings, self.threads, self.stop_event)
        elif component_type == "MSW":
            run_msw(settings, self.threads, self.stop_event)

    def stop(self):
        self.stop_event.set()


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    smart_home = SmartHomeController()
    try:
        for pi_id, pi_settings in settings.items():
            for device_id, device_settings in pi_settings.items():
                smart_home.run_controller(device_settings["type"], device_settings)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping app')
        smart_home.stop()

