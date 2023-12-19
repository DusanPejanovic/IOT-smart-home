from simulation.controllers.controller import Controller
from simulation.controllers.mqtt_publisher import MQTTPublisher
from simulation.simulators.pir_simulator import PIRSimulator


class PirController(Controller):
    def callback(self, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print("Motion detected.")

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.component_id, [('Motion', 1)])

    def run_loop(self):
        if self.settings['simulated']:
            simulator = PIRSimulator(self.callback, self.stop_event)
            print("Starting PIR simulator")
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("Button PIR started")
        else:
            from simulation.sensors.pir_sensor import PIRSensor
            print("Setting up PIR sensor")
            pir_sensor = PIRSensor(self.settings['pin'])
            pir_sensor.setup_motion_detection(self.callback)
            print("PIR sensor is set up and waiting for motion")