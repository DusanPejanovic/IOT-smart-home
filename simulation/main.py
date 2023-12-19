import time

from controllers.btn_controller import ButtonController
from controllers.dht_controller import DHTController
from controllers.msw_controller import MSWController
from controllers.pir_controller import PirController
from controllers.uds_controller import UDSController
from settings import load_settings
from simulation.controllers.controller import Controller

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

threads = []


def run_controller(pi_id, component_id, settings):
    component_type = settings["type"]
    if component_type == "PIR":
        pir_controller = PirController(pi_id, component_id, settings, threads)
        pir_controller.run_loop()
    elif component_type == "UDS":
        uds_controller = UDSController(pi_id, component_id, settings, threads)
        uds_controller.run_loop()
    elif component_type == "BTN":
        button_controller = ButtonController(pi_id, component_id, settings, threads)
        button_controller.run_loop()
    elif component_type == "DHT":
        dht_controller = DHTController(pi_id, component_id, settings, threads)
        dht_controller.run_loop()
    elif component_type == "MSW":
        msw_controller = MSWController(pi_id, component_id, settings, threads)
        msw_controller.run_loop()


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    try:
        for pi_id, pi_settings in settings.items():
            for component_id, component_settings in pi_settings.items():
                run_controller(pi_id, component_id, component_settings)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping app')
        Controller.stop_event.set()
        for t in threads:
            t.join()
    finally:
        try:
            GPIO.cleanup()
        except:
            pass
