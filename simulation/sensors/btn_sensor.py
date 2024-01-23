import RPi.GPIO as GPIO


class ButtonSensor:
    def __init__(self, pin):
        self.pin = pin
        self.setup()

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setup_event_detect(self, callback, bouncetime=200):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=lambda x: callback(True), bouncetime=bouncetime)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda x: callback(False), bouncetime=bouncetime)
