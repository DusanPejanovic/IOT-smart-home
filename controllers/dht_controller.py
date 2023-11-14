import threading
import time

from sensors.simulation.dht_simulation import run_dht_simulator


class DHTController:
    def __init__(self, pi_id, component_id, settings):
        self.pi_id = pi_id
        self.component_id = component_id
        self.settings = settings

    def callback(self, humidity, temperature):
        t = time.localtime()
        print("= " * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Pi id: {self.pi_id}%")
        print(f"Code: {self.component_id}%")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    def run(self, threads, stop_event):
        if self.settings['simulated']:
            print(f"Starting {self.component_id} simulation")
            thread = threading.Thread(target=run_dht_simulator, args=(2, self.callback, stop_event))
        else:
            from sensors.dht import run_dht_loop, DHT
            print(f"Starting {self.component_id} loop")
            dht = DHT(self.settings)
            thread = threading.Thread(target=run_dht_loop, args=(dht, 2, self.callback, stop_event))

        thread.start()
        threads.append(thread)
        print(f"{self.component_id} loop started")
