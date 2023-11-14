from simulators.dht_simulator import DHTSimulator
import threading
import time


def dht_callback(humidity, temperature):
    with threading.Lock():
        t = time.localtime()
        print(f"Humidity: {humidity}% Temperature: {temperature}°C {time.strftime('%H:%M:%S', t)}")


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting dht1 sumilator")
        simulator = DHTSimulator(dht_callback, stop_event)
        sim_thread = simulator.start()
        threads.append(sim_thread)
        print("Dht1 sumilator started")
    else:
        from sensors.dht_sensor import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")
