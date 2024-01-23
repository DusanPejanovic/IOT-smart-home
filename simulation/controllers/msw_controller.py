import threading

from controllers.controller import Controller
from simulators.msw_simulator import simulate_membrane_switch


class MSWController(Controller):
    def callback(self, key, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print("Membrane switch activated.")

        self.publish_measurements([('Key', key)])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_membrane_switch, args=(2, self.callback, self.stop_event))
        else:
            from sensors.msw_sensor import MembraneSwitch, run_membrane_switch_loop
            switch = MembraneSwitch(self.settings['pin'], self.settings['r_pins'], self.settings['c_pins'])
            thread = threading.Thread(target=run_membrane_switch_loop, args=(switch, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)