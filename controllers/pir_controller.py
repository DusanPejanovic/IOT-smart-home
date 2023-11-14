import threading
from simulators.pir_simulator import PIRSimulator
import time


def motion_detected():
    t = time.localtime()
    print(f"Motion detected. {time.strftime('%H:%M:%S', t)}")


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting PIR simulator")
        simulator = PIRSimulator(motion_detected, stop_event)
        sim_thread = simulator.start()
        threads.append(sim_thread)
        print("PIR simulator started")
    else:
        from sensors.pir_sensor import PIRSensor
        print("Setting up PIR sensor")
        pir_sensor = PIRSensor(settings['pin'])
        pir_sensor.setup_motion_detection(motion_detected)
        print("PIR sensor is set up and waiting for motion")
