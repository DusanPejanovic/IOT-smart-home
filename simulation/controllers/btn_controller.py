import threading

from controllers.controller import Controller
from simulators.btn_simulator import simulate_button_press


class ButtonController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, ds_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.ds_callback = ds_callback

    def callback(self, pressed):
        self.publish_measurements([('Button', int(pressed))])
        self.ds_callback()

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_button_press, args=(self.callback, self.stop_event))
            thread.start()
            self.threads.append(thread)
        else:
            from sensors.btn_sensor import ButtonSensor
            button_sensor = ButtonSensor(self.settings['pin'])
            button_sensor.setup_event_detect(self.callback)
