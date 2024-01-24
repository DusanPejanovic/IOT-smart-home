import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class LEDController:
    def __init__(self, pi_id, name, simulated, pin=0):
        self.pi_id = pi_id
        self.name = name
        self.led_on = False
        self.simulated = simulated
        self.pin = pin
        if not simulated:
            self.setup_led_actuator()

    def setup_led_actuator(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def led_info(self):
        with threading.Lock():
            t = time.localtime()
            print()
            print("= " * 20)
            print(f"Pi id: {self.pi_id}")
            print(f"Component name: {self.name}")
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if self.led_on:
                print(f"Led turned on!")
            else:
                print(f"Led turned off!")

    def turn_on(self):
        self.led_on = True
        if not self.simulated:
            GPIO.output(self.pin, GPIO.HIGH)
        MQTTPublisher.process_and_batch_measurements(self.pi_id,
                                                     self.name,
                                                     [("Led", int(self.led_on))],
                                                     self.simulated)

    def turn_off(self):
        self.led_on = False
        if not self.simulated:
            GPIO.output(self.pin, GPIO.LOW)
        MQTTPublisher.process_and_batch_measurements(self.pi_id,
                                                     self.name,
                                                     [("Led", int(self.led_on))],
                                                     self.simulated)
