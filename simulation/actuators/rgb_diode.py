import RPi.GPIO as GPIO
import time
import random


class RGBDiode:
    def __init__(self, id, red_pin, green_pin, blue_pin):
        self.id = id
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        self.setup()

    def setup(self):
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def turn_white(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def turn_blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def turn_red(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def turn_green(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def turn_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)


def run_rgb_diode_loop(rgb_diode, delay, callback, stop_event):
    color_actions = {
        "Red": (rgb_diode.turn_red, 0.2),
        "Blue": (rgb_diode.turn_blue, 0.4),
        "Green": (rgb_diode.turn_green, 0.6),
        "White": (rgb_diode.turn_white, 0.8),
        "Off": (rgb_diode.turn_off, 1.0)
    }

    while not stop_event.is_set():
        time.sleep(delay)
        rnd = random.random()
        for color, (action, threshold) in color_actions.items():
            if rnd < threshold:
                action()
                callback(color)
                break
