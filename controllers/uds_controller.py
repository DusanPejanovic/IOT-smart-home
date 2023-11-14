import threading
import time

from simulators.uds_simulator import UDSSimulator


def uds_callback(distance):
    t = time.localtime()
    print(f"Distance: {distance}% {time.strftime('%H:%M:%S', t)}")


def run_uds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting UDS sumilator")
        simulator = UDSSimulator(uds_callback, stop_event)
        sim_thread = simulator.start()
        threads.append(sim_thread)
        print("UDS sumilator started")
    else:
        from sensors.uds_sensor import run_uds_loop, UDSSensor
        print("Starting UDS loop")
        uds = UDSSensor(settings["trigger_pin"], settings["echo_pin"])
        uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print("UDS loop started")
