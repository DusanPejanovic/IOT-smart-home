import threading
from datetime import datetime

from controllers.btn_controller import ButtonController
from controllers.buzzer_controller import BuzzerController
from controllers.controller import Controller
from controllers.dht_controller import DHTController
from controllers.led_controller import LEDController
from controllers.msw_controller import MSWController
from controllers.pir_controller import PirController
from controllers.uds_controller import UDSController
from system_logic.alarm import Alarm
from system_logic.alarm_clock import AlarmClock
from utility.thread_safe_objects import Counter, Text


class SmartHome:
    def __init__(self):
        self.actuators = {}
        self.sensors = {}
        self.threads = []

        self.detected_people = Counter(0)
        self.uds_measurements = {"DUS1": [], "DUS2": []}
        self.gsg_measurements = []
        self.pin_entered = Text("")

        # Run AlarmClock thread
        alarm_clock_thread = threading.Thread(target=AlarmClock.check_alarm, args=(Controller.stop_event,))
        alarm_clock_thread.start()
        self.threads.append(alarm_clock_thread)

    def create_controller(self, pi_id, component_type, component_id, settings):
        if component_type == "DHT":
            self.sensors[component_id] = (DHTController(pi_id, component_id, settings, self.threads))
        elif component_type == "UDS":
            self.sensors[component_id] = (UDSController(pi_id, component_id, settings, self.threads, self.uds_callback))
        elif component_type == "PIR":
            self.sensors[component_id] = (PirController(pi_id, component_id, settings, self.threads, self.pir_callback))
        elif component_type == "BTN":
            self.sensors[component_id] = (ButtonController(pi_id, component_id, settings, self.threads, self.ds_callback))
        elif component_type == "MSW":
            self.sensors[component_id] = (MSWController(pi_id, component_id, settings, self.threads, self.dms_callback))
        elif component_type == "LED":
            self.actuators[component_id] = (LEDController(pi_id, component_id, settings, self.threads))
        elif component_type == "BZR":
            self.actuators[component_id] = (BuzzerController(pi_id, component_id, settings, self.threads))
        else:
            raise ValueError(f"Unknown component type: {component_type}")

    def start(self):
        for controller in self.sensors.values():
            controller.run_loop()

    def pir_callback(self, pir_id):
        pir_id_map = {
            "DPIR1": ["DL1", "DUS1"],
            "DPIR2": ["DL2", "DUS2"]
        }

        # If DPIR has detected
        if pir_id in pir_id_map.keys():
            led_id, uds_id = pir_id_map[pir_id]

            try:
                # Turn on led for 10 seconds
                led_simulation = threading.Thread(target=self.actuators[led_id].turn_on_off_simulation, args=())
                led_simulation.start()
                self.threads.append(led_simulation)

                # Update detected people count
                measurements = self.uds_measurements[uds_id]
                if len(measurements) >= 4:
                    last_measurement = measurements[-1]['distance']
                    recent_average = sum(m['distance'] for m in measurements[-4:-1]) / 3

                    if last_measurement < recent_average:
                        self.detected_people.increment()
                    else:
                        self.detected_people.decrement()

                    print("Detected people count:", self.detected_people.get_value())
            except KeyError:
                print(f"Error: Invalid LED or UDS ID for PIR sensor {pir_id}")

        # If RPIR has detected
        if pir_id in ["RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
            if self.detected_people.get_value() == 0:
                Alarm.activate_alarm("Pir has detected.")

    def uds_callback(self, uds_id, distance):
        self.uds_measurements[uds_id].append({'distance': distance, 'timestamp': datetime.now()})

    def ds_callback(self):
        if Alarm.system_activated() and self.pin_entered.get_value() != Alarm.get_pin():
            print("USO")
            Alarm.activate_alarm("Ds sensor activated and wrong pin!")

    def dms_callback(self, key):
        self.pin_entered.append(key)
        if self.pin_entered.get_value() == Alarm.get_pin():
            if not Alarm.system_activated():
                Alarm.activate_system()
            elif Alarm.alarm_activated():
                Alarm.deactivate_alarm()

    def gsg_callback(self, acceleration, rotation):
        acceleration_magnitude = sum([x ** 2 for x in acceleration]) ** 0.5
        angular_velocity_magnitude = sum([x ** 2 for x in rotation]) ** 0.5
        if acceleration_magnitude + angular_velocity_magnitude > 10:
            pass
            # self.turn_on_alarm()

    def dht_callback(self, dht_id, humidity, temperature):
        if dht_id == "GDHT":
            self.actuators["GLCD"].display_dht_values(temperature, humidity)
