import threading

from controllers.controller import Controller
from MQTT.mqtt_publisher import MQTTPublisher
from simulators.btn_simulator import simulate_button_press


class ButtonController(Controller):
    def callback(self, pressed, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                if pressed:
                    print("Button pressed!")
                else:
                    print("Button released!")
        self.publish_measurements([('Button', int(pressed))])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_button_press, args=(self.callback, self.stop_event))
            thread.start()
            self.threads.append(thread)
        else:
            from sensors.btn_sensor import ButtonSensor
            button_sensor = ButtonSensor(self.settings['pin'])
            button_sensor.setup_event_detect(self.callback)
