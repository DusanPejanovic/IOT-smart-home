import RPi.GPIO as GPIO


class DS:
    def __init__(self, button_port):
        self.button_port = button_port

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO.BCM, self.button_port, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detection(self.button_port, GPIO.RISING, callback=self.button_pressed, bouncetime=100)

    def button_pressed(self):
        print("Button pressed.")
