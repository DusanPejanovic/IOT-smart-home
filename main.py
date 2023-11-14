import threading
import time
import json
from exceptions import UnrecognizedComponentException
from controllers import DHTController

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def create_controller(component_type, pi_id, component_id, settings):
    if component_type == "DHT":
        return DHTController(pi_id, component_id, settings)

    raise UnrecognizedComponentException(component_type)


def load_settings(file_path='settings.json'):
    with open(file_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        for pi_id, pi_settings in settings.items():
            for component_id, component_settings in settings[pi_id].items():
                controller = create_controller(component_settings["component_type"], pi_id, component_id,
                                               component_settings)
                controller.run(threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
