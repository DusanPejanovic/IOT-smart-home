import RPi.GPIO as GPIO
import time


class MembraneSwitch:
    def __init__(self, id, r_pins, c_pins):
        self.id = id
        self.r_pins = r_pins
        self.c_pins = c_pins
        self.setup()

    def setup(self):
        for r_pin in self.r_pins:
            GPIO.setup(r_pin, GPIO.OUT)

        for c_pin in self.c_pins:
            GPIO.setup(c_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def scan_keypad_row(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(self.c_pins[0]) == 1:
            return characters[0]
        if GPIO.input(self.c_pins[1]) == 1:
            return characters[1]
        if GPIO.input(self.c_pins[2]) == 1:
            return characters[2]
        if GPIO.input(self.c_pins[3]) == 1:
            return characters[3]
        GPIO.output(line, GPIO.LOW)


def run_membrane_switch_loop(membrane_switch, delay, callback, stop_event):
    row_characters = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]

    while not stop_event.is_set():
        time.sleep(delay)

        for row_pin, characters in zip(membrane_switch.r_pins, row_characters):
            pressed_key = membrane_switch.scan_keypad_row(row_pin, characters)
            if pressed_key:
                callback(pressed_key)
