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
from system_logic.alarm_clock import AlarmClock
from utility.registry import ControllerRegistry

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass

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
                if component_settings['running']:
                    print(component_settings)
                    smart_home.create_controller(pi_id, component_settings['type'], component_id, component_settings)
        smart_home.start()

        ControllerRegistry().print_controllers()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping app')
        Controller.stop_event.set()
        for i in range(smart_home.threads.get_len()):
            if smart_home.threads.get(i).is_alive():
                smart_home.threads.get(i).join()
    finally:
        try:
            GPIO.cleanup()
        except:
            pass
