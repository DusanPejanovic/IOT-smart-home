from controllers.controller import Controller
from simulators.btn_simulator import ButtonSimulator


class ButtonController(Controller):
    def callback(self):
        with self.console_lock:
            print(self.get_basic_info())
            print("Button pressed!")

    def run_loop(self):
        if self.settings['simulated']:
            simulator = ButtonSimulator(self.callback, self.stop_event)
            print("Starting button simulator")
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("Button simulator started")
        else:
            from sensors.btn_sensor import ButtonSensor
            print("Setting up button sensor")
            button_sensor = ButtonSensor(self.settings['pin'])
            button_sensor.setup_event_detect(self.callback)
            print("Button sensor is set up and waiting for press")
