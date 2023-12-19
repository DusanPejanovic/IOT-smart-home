import threading

from simulation.controllers.controller import Controller
from simulation.controllers.mqtt_publisher import MQTTPublisher
from simulation.simulators.msw_simulator import MembraneSwitchSimulator


class MSWController(Controller):
    def callback(self, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print("Membrane switch activated.")

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.component_id, [('Membrane', 1)])

    def run_loop(self):
        if self.settings['simulated']:
            print("Starting membrane switch simulator")
            simulator = MembraneSwitchSimulator(self.callback, self.stop_event)
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("Membrane switch simulator started")
        else:
            from simulation.sensors.msw_sensor import MembraneSwitch
            print("Starting membrane switch loop")
            switch = MembraneSwitch(self.settings['pin'])
            switch_thread = threading.Thread(target=switch.run_membrane_switch_loop,
                                             args=(self.callback, self.stop_event))
            switch_thread.start()
            self.threads.append(switch_thread)
            print("Membrane switch loop started")
