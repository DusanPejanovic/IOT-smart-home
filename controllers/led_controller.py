import RPi.GPIO as GPIO


class LedController:
    def __init__(self, pin):
        self.pin = pin
        self.curr_state = GPIO.LOW
        self.setup()

    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def switch(self):
        if self.curr_state == GPIO.LOW:
            GPIO.output(self.pin, GPIO.HIGH)
            self.curr_state = GPIO.HIGH
        else:
            GPIO.output(self.pin, GPIO.LOW)
            self.curr_state = GPIO.LOW
