import threading

from controllers.controller import Controller
from simulators.rgb_diode_simulator import simulate_rgb_diode


class RGBDiodeController(Controller):
    def callback(self, text, verbose=False):
        self.publish_measurements([('Text', text)])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_rgb_diode, args=(2, self.callback, self.stop_event))
        else:
            from actuators.rgb_diode import RGBDiode, run_rgb_diode_loop
            rgb_diode = RGBDiode(self.component_id,
                                 self.settings['red_pin'],
                                 self.settings['green_pin'],
                                 self.settings['blue_pin'])
            thread = threading.Thread(target=run_rgb_diode_loop, args=(rgb_diode, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
