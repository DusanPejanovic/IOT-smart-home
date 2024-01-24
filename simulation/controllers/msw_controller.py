import threading

from controllers.controller import Controller
from simulators.msw_simulator import simulate_membrane_switch


class MSWController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, dms_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.dms_callback = dms_callback

    def callback(self, key):
        self.publish_measurements([('Key', key)])
        self.dms_callback(key)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_membrane_switch, args=(2, self.callback, self.stop_event))
        else:
            from sensors.msw_sensor import MembraneSwitch, run_membrane_switch_loop
            switch = MembraneSwitch(self.settings['pin'], self.settings['r_pins'], self.settings['c_pins'])
            thread = threading.Thread(target=run_membrane_switch_loop, args=(switch, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)