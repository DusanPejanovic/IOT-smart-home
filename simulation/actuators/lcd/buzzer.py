import RPi.GPIO as GPIO
import time
import random
import threading


class Buzzer(object):
    def __init__(self, id, pin, pitch):
        self.id = id
        self.pin = pin
        self.pitch = pitch

    def setup_buzzer(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz(self, duration):
        period = 1.0 / self.pitch
        delay = period / 2
        cycles = int(duration * self.pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

    def alarm(self, buzz_duration, alarm_duration):
        for _ in range(alarm_duration // (buzz_duration * 2)):
            self.buzz(buzz_duration)
            time.sleep(buzz_duration)

    def panic(self, buzz_duration, panic_duration):
        for _ in range(panic_duration // (buzz_duration * 2)):
            self.buzz(buzz_duration)

    def turn_on(self):
        GPIO.output(self.pin, True)

    def turn_off(self):
        GPIO.output(self.pin, False)

    def buzz_note(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2.0
        cycles = int(duration * pitch)

        for _ in range(cycles):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(delay)
