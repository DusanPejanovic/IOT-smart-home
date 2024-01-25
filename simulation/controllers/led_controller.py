import threading
import time

from controllers.controller import Controller


class LEDController(Controller):
    def __init__(self, pi_id, component_id, settings, threads):
        super().__init__(pi_id, component_id, settings, threads)

        self.simulated = settings.get('simulated', False)
        if not self.simulated:
            from actuators.led_diode import LedDiode
            self.led = LedDiode(component_id, settings['pin'])
        else:
            self.led = None

        self.led_on = False
        self.led_on_lock = threading.Lock()

    def callback(self, led_on):
        with self.led_on_lock:
            self.led_on = led_on
        self.publish_measurements([("Led", int(led_on))])

    def turn_on(self):
        with self.led_on_lock:
            if self.led_on:
                return

        if not self.simulated:
            self.led.turn_on()

        self.callback(True)

    def turn_off(self):
        with self.led_on_lock:
            if not self.led_on:
                return

        self.callback(False)

    def run_loop(self):
        pass

    def turn_on_off_simulation(self):
        with self.led_on_lock:
            if self.led_on:
                return

        self.turn_on()
        self.turn_off()
