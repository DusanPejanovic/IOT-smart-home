import random
import threading
import time

from controllers.controller import Controller
from simulators.btn_simulator import simulate_button_press


class ButtonController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, ds_callback, release_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.ds_callback = ds_callback
        self.release_callback = release_callback

        self.button_pressed = False

    def callback(self, is_pressed):
        if self.button_pressed == is_pressed:
            return
        self.button_pressed = is_pressed
        self.publish_measurements([('Button', int(self.button_pressed))])

        if is_pressed:
            self.ds_callback(self.component_id)
        else:
            self.release_callback(self.component_id)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_button_press, args=(self.callback, self.stop_event))
        else:
            from sensors.btn_sensor import ButtonSensor
            button = ButtonSensor(self.settings['pin'])
            thread = threading.Thread(target=self.button_check_loop, args=(button,))

        thread.start()
        self.threads.append(thread)

    def button_check_loop(self, button):
        while not self.stop_event.is_set():
            time.sleep(0.5)
            if button.is_pressed():
                self.callback(True)
            else:
                self.callback(False)
