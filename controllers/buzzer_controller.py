import RPi.GPIO as GPIO
import time

from sensors.simulation.dht_simulation import run_dht_simulator


class DHTController:
    def __init__(self, buzzer_pin, component_id, settings):
        self.buzzer_pin = buzzer_pin

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.buzzer_pin, True)
            time.sleep(delay)
            GPIO.output(self.buzzer_pin, False)
            time.sleep(delay)
