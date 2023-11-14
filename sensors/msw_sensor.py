# sensors/membrane_switch.py

import RPi.GPIO as GPIO
import time

class MembraneSwitch:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # This function could be a loop that continuously checks the state of the switch
    def run_membrane_switch_loop(self, callback, stop_event):
        while not stop_event.is_set():
            if GPIO.input(self.pin) == GPIO.LOW:
                callback()
            time.sleep(0.1)  # Add a short delay to prevent bouncing
