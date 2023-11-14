import threading
import time

from simulators.btn_simulator import ButtonSimulator


def button_pressed():
    t = time.localtime()
    print(f"Button press. {time.strftime('%H:%M:%S', t)}")


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting button simulator")
        simulator = ButtonSimulator(button_pressed, stop_event)
        sim_thread = simulator.start()
        threads.append(sim_thread)
        print("Button simulator started")
    else:
        from sensors.btn_sensor import ButtonSensor
        print("Setting up button sensor")
        button_sensor = ButtonSensor(settings['pin'])
        button_sensor.setup_event_detect(button_pressed)

        print("Button sensor is set up and waiting for press")
