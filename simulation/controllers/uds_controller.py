import threading

from controllers.controller import Controller
from simulators.uds_simulator import simulate_uds_distance


class UDSController(Controller):
    def callback(self, distance, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print(f"Distance: {distance}%")

        self.publish_measurements([('Distance', distance)])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_uds_distance, args=(self.callback, self.stop_event))
        else:
            from sensors.uds_sensor import run_uds_loop, UDSSensor
            uds = UDSSensor(self.settings["trigger_pin"], self.settings["echo_pin"])
            thread = threading.Thread(target=run_uds_loop, args=(uds, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
