import RPi.GPIO as GPIO


class LedDiode:
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin
        self.setup()

    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
