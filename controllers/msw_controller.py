import threading
from simulators.msw_simulator import MembraneSwitchSimulator
import time

def switch_activated():
    t = time.localtime()
    print(f"Membrane switch activated. {time.strftime('%H:%M:%S', t)}")

def run_msw(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting membrane switch simulator")
        simulator = MembraneSwitchSimulator(switch_activated, stop_event)
        sim_thread = simulator.start()
        threads.append(sim_thread)
        print("Membrane switch simulator started")
    else:
        from sensors.msw_sensor import MembraneSwitch
        print("Starting membrane switch loop")
        switch = MembraneSwitch(settings['pin'])
        switch_thread = threading.Thread(target=switch.run_membrane_switch_loop, args=(switch_activated, stop_event))
        switch_thread.start()
        threads.append(switch_thread)
        print("Membrane switch loop started")