import threading

from controllers.controller import Controller
from simulators.pir_simulator import simulate_pir_motion


class PirController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, pir_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.pir_callback = pir_callback

    def callback(self):
        self.publish_measurements([('Motion', 1)])
        self.pir_callback(self.component_id)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_pir_motion, args=(self.callback, self.stop_event))
            thread.start()
            self.threads.append(thread)
        else:
            from sensors.pir_sensor import PIRSensor
            pir_sensor = PIRSensor(self.settings['pin'])
            pir_sensor.setup_motion_detection(self.callback)
