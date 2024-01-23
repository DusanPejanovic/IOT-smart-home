import RPi.GPIO as GPIO


class PIRSensor:
    def __init__(self, pin):
        self.pin = pin
        self.setup()

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN)

    def setup_motion_detection(self, callback, bouncetime=200):
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=callback, bouncetime=bouncetime)
