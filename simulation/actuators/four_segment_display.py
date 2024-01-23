import RPi.GPIO as GPIO
import time

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}


class FourSegmentDisplay:
    def __init__(self, id, segment_pins, digital_pins):
        self.id = id
        self.segment_pins = segment_pins
        self.digit_pins = digital_pins
        self.setup()

    def setup(self):
        for segment in self.segment_pins:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in self.digit_pins:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    def display_time(self, s_time):
        for digit in range(4):
            for loop in range(0, 7):
                GPIO.output(self.segment_pins[loop], num[s_time[digit]][loop])
                if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(self.digit_pins[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digit_pins[digit], 1)


def show_time_on_four_segment_display(segment_display, delay, callback, stop_event):
    while not stop_event.is_set():
        time.sleep(delay)

        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)

        segment_display.display_time(s)
        callback(s[0], s[1], s[2], s[3])
