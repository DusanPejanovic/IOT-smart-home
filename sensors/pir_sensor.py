import RPi.GPIO as GPIO


# PIR sensor class
class PIRSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def setup_motion_detection(self, motion_callback, bouncetime=200):
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=motion_callback, bouncetime=bouncetime)

