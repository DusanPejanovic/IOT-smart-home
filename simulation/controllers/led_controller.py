import threading
import time

from simulation.controllers.mqtt_publisher import MQTTPublisher


class LedController:
    def __init__(self, pi_id, name, simulated, pin=0):
        self.pi_id = pi_id
        self.name = name
        self.led_on = False
        self.simulated = simulated
        self.pin = pin
        if not simulated:
            self.setup_led_actuator()

    def setup_led_actuator(self):
        import RPi.GPIO as GPIO
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

    def change_led_state(self):
        if self.simulated:
            self.led_on = not self.led_on
            self.led_info()
        else:
            import RPi.GPIO as GPIO
            if not self.led_on:
                GPIO.output(self.pin, GPIO.HIGH)
                self.led_on = False
            else:
                GPIO.output(self.pin, GPIO.LOW)
                self.led_on = True

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.name, [("Led", int(self.led_on))], self.simulated)
