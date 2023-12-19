import threading
import time

from simulation.controllers.mqtt_publisher import MQTTPublisher


class BuzzerController:
    def __init__(self, pi_id, name, simulated, pin=0):
        self.pi_id = pi_id
        self.name = name
        self.buzzer_on = False
        self.simulated = simulated
        self.pin = pin
        self.buzz = None
        if not simulated:
            self.setup_buzzer()

    def setup_buzzer(self):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.buzz = GPIO.PWM(self.pin, 440)

    def buzzer_info(self):
        with threading.Lock():
            t = time.localtime()
            print()
            print("= " * 20)
            print(f"Pi id: {self.pi_id}")
            print(f"Component name: {self.name}")
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if self.buzzer_on:
                print(f"Buzzer turned on!")
            else:
                print(f"Buzzer turned off!")

    def change_buzzer_state(self):
        if self.simulated:
            self.buzzer_on = not self.buzzer_on
            self.buzzer_info()
        else:
            import RPi.GPIO as GPIO
            if not self.buzzer_on:
                self.buzz.start(50)
                self.buzzer_on = False
            else:
                self.buzz.stop()
                self.buzzer_on = True

        print("Evo ga", int(self.buzzer_on))

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.name, [("Buzzer", int(self.buzzer_on))],
                                                     self.simulated)
