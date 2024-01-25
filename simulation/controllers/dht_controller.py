import threading

from controllers.controller import Controller
from simulators.dht_simulator import simulate_humidity_and_temperature


class DHTController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, dht_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.dht_callback = dht_callback

    def callback(self, humidity, temperature):
        self.publish_measurements([('Humidity', humidity), ('Temperature', temperature)])
        self.dht_callback(self.component_id, humidity, temperature)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_humidity_and_temperature, args=(self.callback, self.stop_event))
        else:
            from sensors.dht_sensor import run_dht_loop, DHT
            dht = DHT(self.settings['pin'])
            thread = threading.Thread(target=run_dht_loop, args=(dht, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
