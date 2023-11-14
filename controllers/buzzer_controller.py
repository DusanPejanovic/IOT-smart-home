import threading
import time


class BuzzerController:
    def __init__(self, pi_id, name, simulated, pin=0):
        self.pi_id = pi_id
        self.name = name
        self.buzzer_on = False
        self.simulated = simulated
        self.pin = pin
        if not simulated:
            self.setup_buzzer()

    def setup_buzzer(self):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

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
                GPIO.output(self.pin, GPIO.HIGH)
                self.buzzer_on = False
            else:
                GPIO.output(self.pin, GPIO.LOW)
                self.buzzer_on = True

