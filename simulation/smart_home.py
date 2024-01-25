import json
import math
import threading
import time
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt

from broker_settings import HOSTNAME, PORT
from controllers.btn_controller import ButtonController
from controllers.buzzer_controller import BuzzerController
from controllers.controller import Controller
from controllers.dht_controller import DHTController
from controllers.gyro_controller import GyroController
from controllers.led_controller import LEDController
from controllers.msw_controller import MSWController
from controllers.pir_controller import PirController
from controllers.uds_controller import UDSController
from system_logic.alarm import Alarm
from system_logic.alarm_clock import AlarmClock
from utility.thread_safe_objects import Counter, Text, ThreadSafeList


class SmartHome:
    def __init__(self):
        self.actuators = {}
        self.sensors = {}
        self.threads = ThreadSafeList()

        self.detected_people = Counter(0)
        self.uds_measurements = {"DUS1": [], "DUS2": []}
        self.gsg_measurements = []
        self.pin_entered = Text("")

        self.last_ds1_release = datetime.now()
        self.last_ds2_release = datetime.now()

        # Run AlarmClock thread
        alarm_clock_thread = threading.Thread(target=AlarmClock.check_alarm, args=(Controller.stop_event,))
        alarm_clock_thread.start()
        self.threads.append(alarm_clock_thread)

        # Run Alarm thread
        alarm_thread = threading.Thread(target=Alarm.run_loop, args=(Controller.stop_event,))
        alarm_thread.start()
        self.threads.append(alarm_thread)

        # Subscribe buzzer callback
        Alarm.add_alarm_activation_listener(self.alarm_buzzer_check)
        AlarmClock.add_alarm_clock_activation_listener(self.alarm_clock_buzzer_check)

        # MQTT client initialization
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message

        # Connect to MQTT broker
        self.connect_to_mqtt_broker()

    def connect_to_mqtt_broker(self):
        mqtt_broker_address = HOSTNAME
        mqtt_broker_port = PORT
        self.mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 60)

        # Start MQTT loop in a separate thread
        mqtt_thread = threading.Thread(target=self.mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe("clock-alarm/on")
        self.mqtt_client.subscribe("clock-alarm/off")
        self.mqtt_client.subscribe("alarm/off")
        self.mqtt_client.subscribe("rgb/color")

    def on_mqtt_message(self, client, userdata, msg):
        if msg.topic == "clock-alarm/on":
            # Set the alarm
            payload = json.loads(msg.payload.decode())
            start_datetime = datetime.strptime(f"{payload['date']} {payload['time']}", "%Y-%m-%d %H:%M")
            AlarmClock.set_alarm(start_datetime)
        elif msg.topic == "clock-alarm/off":
            # Turn off Alarm
            AlarmClock.turn_off()
        elif msg.topic == "alarm/off":
            Alarm.deactivate_alarm()
        elif msg.topic == "rgb/color":
            payload = json.loads(msg.payload.decode())
            color = payload['color']
            if color == "OFF":
                self.actuators['BRGB'].turn_off()
            elif color == "ON":
                self.actuators['BRGB'].turn_on()
            else:
                self.actuators['BRGB'].change_color(color)

    def create_controller(self, pi_id, component_type, component_id, settings):
        if component_type == "DHT":
            self.sensors[component_id] = (DHTController(pi_id, component_id, settings, self.threads))
        elif component_type == "UDS":
            self.sensors[component_id] = (UDSController(pi_id, component_id, settings, self.threads, self.uds_callback))
        elif component_type == "PIR":
            self.sensors[component_id] = (PirController(pi_id, component_id, settings, self.threads, self.pir_callback))
        elif component_type == "BTN":
            self.sensors[component_id] = (
                ButtonController(pi_id, component_id, settings, self.threads, self.ds_callback,
                                 self.last_released_time))
        elif component_type == "MSW":
            self.sensors[component_id] = (MSWController(pi_id, component_id, settings, self.threads, self.dms_callback))
        elif component_type == "LED":
            self.actuators[component_id] = (LEDController(pi_id, component_id, settings, self.threads))
        elif component_type == "BZR":
            self.actuators[component_id] = (BuzzerController(pi_id, component_id, settings, self.threads))
        elif component_type == "GSG":
            self.sensors[component_id] = (GyroController(pi_id, component_id, settings, self.threads))
        else:
            raise ValueError(f"Unknown component type: {component_type}")

    def start(self):
        for (component_id, controller) in self.sensors.items():
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

    def ds_callback(self, ds_id):
        if Alarm.system_activated() and self.pin_entered.get_value() != Alarm.get_pin():
            Alarm.activate_alarm("Wrong pin!")

        if ds_id == "DS1" and datetime.now() - self.last_ds1_release > timedelta(seconds=5):
            Alarm.activate_alarm("DS1 held for too long!")
        elif ds_id == "DS2" and datetime.now() - self.last_ds2_release > timedelta(seconds=5):
            Alarm.activate_alarm("DS2 held for too long!")

    def last_released_time(self, ds_id):
        if ds_id == "DS1":
            self.last_ds1_release = datetime.now()
            if Alarm.alarm_activated() and Alarm.get_reason() == "DS1 held for too long!":
                Alarm.deactivate_alarm()
        elif ds_id == "DS2":
            self.last_ds2_release = datetime.now()
            if Alarm.get_reason() == "DS2 hold for too long!":
                Alarm.deactivate_alarm()

    def dms_callback(self, key):
        self.pin_entered.append(key)
        if self.pin_entered.get_value() == Alarm.get_pin():
            if not Alarm.system_activated():
                Alarm.activate_system()
            elif Alarm.alarm_activated():
                Alarm.deactivate_alarm()

    def calculate_magnitude(self, elements):
        return math.sqrt(sum(i ** 2 for i in elements))

    def gsg_callback(self, acceleration, rotation):
        if len(self.gsg_measurements) > 0:
            if abs(self.calculate_magnitude(acceleration) - self.calculate_magnitude(
                    self.gsg_measurements[-1][0]) > 1000):
                Alarm.activate_alarm("Gsg has detected a significant movement!")
            elif abs(
                    self.calculate_magnitude(rotation) - self.calculate_magnitude(self.gsg_measurements[-1][1]) > 1000):
                Alarm.activate_alarm("Gsg has detected a significant movement!")

        self.gsg_measurements.append([acceleration, rotation])

    def dht_callback(self, dht_id, humidity, temperature):
        if dht_id == "GDHT":
            self.actuators["GLCD"].display_dht_values(temperature, humidity)

    def alarm_buzzer_check(self):
        # Door Buzzer
        door_buzzer = self.actuators['DB']
        door_buzzer_thread = threading.Thread(target=door_buzzer.run_alarm_buzzer, args=(Controller.stop_event,))
        door_buzzer_thread.start()
        self.threads.append(door_buzzer_thread)

        # Bedroom Buzzer
        bedroom_buzzer = self.actuators['BB']
        bedroom_buzzer = threading.Thread(target=bedroom_buzzer.run_alarm_buzzer, args=(Controller.stop_event,))
        bedroom_buzzer.start()
        self.threads.append(bedroom_buzzer)

    def alarm_clock_buzzer_check(self):
        # Bedroom Buzzer
        bedroom_buzzer = self.actuators['BB']
        bedroom_buzzer = threading.Thread(target=bedroom_buzzer.run_alarm_clock_buzzer, args=(Controller.stop_event,))
        bedroom_buzzer.start()
        self.threads.append(bedroom_buzzer)
