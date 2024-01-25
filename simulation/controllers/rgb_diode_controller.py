import threading

from controllers.controller import Controller
from simulators.rgb_diode_simulator import simulate_rgb_diode


class RGBDiodeController(Controller):
    def __init__(self, pi_id, component_id, settings, threads):
        super().__init__(pi_id, component_id, settings, threads)

        self.simulated = settings.get('simulated', False)
        if not self.simulated:
            from actuators.rgb_diode import RGBDiode
            self.rgb_diode = RGBDiode(component_id, settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        else:
            self.rgb_diode = None
        self.color = "RED"
        self.led_on = False

    def callback(self, color, state):
        self.color = color
        self.led_on = state
        self.publish_measurements([('Color', color), ('Active', self.led_on)])

    def turn_on(self):
        if self.led_on:
            return

        if not self.simulated:
            if self.color == "RED":
                self.rgb_diode.turn_red()
            elif self.color == "GREEN":
                self.rgb_diode.turn_green()
            elif self.color == "BLUE":
                self.rgb_diode.turn_blue()
            elif self.color == "WHITE":
                self.rgb_diode.turn_white()

        self.callback(self.color, True)

    def turn_off(self):
        if not self.led_on:
            return

        if not self.simulated:
            self.rgb_diode.turn_off()

        self.callback(self.color, False)

    def switch_state(self):
        self.led_on = not self.led_on
        if not self.simulated:
            if self.led_on:
                self.rgb_diode.turn_off()
            else:
                self.rgb_diode.turn_on()

        self.callback(self.color, self.led_on)

    def change_color(self, color):
        if self.color == color:
            return

        if not self.simulated and self.led_on:
            if self.color == "RED":
                self.rgb_diode.turn_red()
            elif self.color == "GREEN":
                self.rgb_diode.turn_green()
            elif self.color == "BLUE":
                self.rgb_diode.turn_blue()
            elif self.color == "WHITE":
                self.rgb_diode.turn_white()

        self.callback(color, self.led_on)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_rgb_diode, args=(2, self.callback, self.stop_event))
            thread.start()
            self.threads.append(thread)
