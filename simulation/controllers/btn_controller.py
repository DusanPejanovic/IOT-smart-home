from simulation.controllers.controller import Controller
from simulation.controllers.mqtt_publisher import MQTTPublisher
from simulation.simulators.btn_simulator import ButtonSimulator


class ButtonController(Controller):
    def callback(self, verbose=False, simulated=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print("Button pressed!")

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.component_id, [('Button', 1)], simulated)

    def run_loop(self):
        if self.settings['simulated']:
            simulator = ButtonSimulator(self.callback, self.stop_event)
            print("Starting button simulator")
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("Button simulator started")
        else:
            from simulation.sensors.btn_sensor import ButtonSensor
            print("Setting up button sensor")
            button_sensor = ButtonSensor(self.settings['pin'])
            button_sensor.setup_event_detect(self.callback)
            print("Button sensor is set up and waiting for press")
