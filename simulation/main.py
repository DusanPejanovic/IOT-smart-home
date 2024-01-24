import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher
from controllers.btn_controller import ButtonController
from controllers.dht_controller import DHTController
from controllers.msw_controller import MSWController
from controllers.pir_controller import PirController
from controllers.uds_controller import UDSController
from settings import load_settings
from controllers.controller import Controller
from smart_home import SmartHome
from utility.registry import ControllerRegistry

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

threads = []


def create_controller(component_type, pi_id, component_id, settings):
    if component_type == "DHT":
        return DHTController(pi_id, component_id, settings, threads)
    elif component_type == "UDS":
        return UDSController(pi_id, component_id, settings, threads)
    elif component_type == "PIR":
        return PirController(pi_id, component_id, settings, threads)
    elif component_type == "BTN":
        return ButtonController(pi_id, component_id, settings, threads)
    elif component_type == "MSW":
        return MSWController(pi_id, component_id, settings, threads)
    else:
        raise ValueError(f"Unknown component type: {component_type}")


def run_controller(pi_id, component_id, settings):
    if settings["type"] == "LED" or settings["type"] == "BZR":
        return

    controller = create_controller(settings["type"], pi_id, component_id, settings)
    controller.run_loop()


if __name__ == "__main__":
    settings = load_settings()

    # Run MQTT publisher thread
    publisher_thread = threading.Thread(target=MQTTPublisher.publisher_task, args=())
    publisher_thread.daemon = True
    publisher_thread.start()

    smart_home = SmartHome()

    try:
        for pi_id, pi_settings in settings.items():
            for component_id, component_settings in pi_settings.items():
                smart_home.create_controller(pi_id, component_settings['type'], component_id, component_settings)
        smart_home.start()

        ControllerRegistry().print_controllers()
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
