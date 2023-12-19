import threading

from simulation.controllers.controller import Controller
from simulation.controllers.mqtt_publisher import MQTTPublisher
from simulation.simulators.dht_simulator import DHTSimulator


class DHTController(Controller):
    def callback(self, humidity, temperature, verbose=False, simulated=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print(f"Humidity: {humidity}%")
                print(f"Temperature: {temperature}°C")

        MQTTPublisher.process_and_batch_measurements(self.pi_id, self.component_id,
                                                     [('Humidity', humidity), ('Temperature', temperature)], simulated)

    def run_loop(self):
        if self.settings['simulated']:
            simulator = DHTSimulator(self.callback, self.stop_event)
            print("Starting button simulator")
            sim_thread = simulator.start()
            self.threads.append(sim_thread)
            print("Button simulator started")
        else:
            from simulation.sensors.dht_sensor import run_dht_loop, DHT
            print("Starting dht1 loop")
            dht = DHT(self.settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, self.callback, self.stop_event))
            dht1_thread.start()
            self.threads.append(dht1_thread)
            print("Dht1 loop started")
