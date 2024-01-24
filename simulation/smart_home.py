import time
from datetime import datetime

from controllers.btn_controller import ButtonController
from controllers.buzzer_controller import BuzzerController
from controllers.dht_controller import DHTController
from controllers.led_controller import LEDController
from controllers.msw_controller import MSWController
from controllers.pir_controller import PirController
from controllers.uds_controller import UDSController


class SmartHome:
    def __init__(self):
        self.actuators = {}
        self.sensors = {}
        self.threads = []

        self.detected_people = 0
        self.uds_measurements = {"DUS1": []}

    def create_controller(self, pi_id, component_type, component_id, settings):
        if component_type == "DHT":
            self.sensors[component_id] = (DHTController(pi_id, component_id, settings, self.threads))
        elif component_type == "UDS":
            self.sensors[component_id] = (UDSController(pi_id, component_id, settings, self.threads))
        elif component_type == "PIR":
            self.sensors[component_id] = (PirController(pi_id, component_id, settings, self.threads, self.pir_callback))
        elif component_type == "BTN":
            self.sensors[component_id] = (ButtonController(pi_id, component_id, settings, self.threads))
        elif component_type == "MSW":
            self.sensors[component_id] = (MSWController(pi_id, component_id, settings, self.threads))
        elif component_type == "LED":
            self.actuators[component_id] = (LEDController(pi_id, component_id, settings['simulated'], self.threads))
        elif component_type == "BZR":
            self.actuators[component_id] = (BuzzerController(pi_id, component_id, settings['simulated'], self.threads))
        else:
            raise ValueError(f"Unknown component type: {component_type}")

    def start(self):
        for controller in self.sensors.values():
            controller.run_loop()

    def turn_on_alarm(self):
        pass

    def pir_callback(self, pir_id):
        pir_id_map = {
            "DPIR1": ["DL1", "DUS1"],
            "DPIR2": ["DL2", "DUS2"]
        }

        # If DPIR has detected
        if pir_id in pir_id_map.keys():
            led_id, uds_id = pir_id_map[pir_id]

            try:
                measurements = self.uds_measurements[uds_id]
                if len(measurements) >= 4:
                    last_measurement = measurements[-1]['distance']
                    recent_average = sum(m['distance'] for m in measurements[-4:-1]) / 3

                    if last_measurement < recent_average:
                        self.detected_people += 1
                    else:
                        self.detected_people = max(0, self.detected_people - 1)

                self.actuators[led_id].turn_on()
                time.sleep(10)
                self.actuators[led_id].turn_off()
            except KeyError:
                print(f"Error: Invalid LED or UDS ID for PIR sensor {pir_id}")

        # if RPIR has detected
        if pir_id in ["RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
            if self.detected_people == 0:
                self.turn_on_alarm()

    def uds_callback(self, uds_id, distance):
        timestamp = datetime.now()
        self.uds_measurements[uds_id].append({'distance': distance, 'timestamp': timestamp})

    def ds_callback(self, uds_id, distance):
        timestamp = datetime.now()
        self.uds_measurements[uds_id].append({'distance': distance, 'timestamp': timestamp})
