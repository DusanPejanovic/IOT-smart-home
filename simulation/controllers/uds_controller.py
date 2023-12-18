import threading

from simulation.controllers.controller import Controller
from simulation.simulators.uds_simulator import UDSSimulator


class UDSController(Controller):
    def callback(self, distance, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print(f"Distance: {distance}%")

        self.process_and_batch_measurements([('Distance', distance)])

    def run_loop(self):
        if self.settings['simulated']:
            print("Starting UDS sumilator")
            simulator = UDSSimulator(self.callback, self.stop_event)
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("UDS sumilator started")
        else:
            from simulation.sensors.uds_sensor import run_uds_loop, UDSSensor
            print("Starting UDS loop")
            uds = UDSSensor(self.settings["trigger_pin"], self.settings["echo_pin"])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, self.callback, self.stop_event))
            uds_thread.start()
            self.threads.append(uds_thread)
            print("UDS loop started")
