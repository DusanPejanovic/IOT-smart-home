import threading

from controllers.controller import Controller
from simulators.ir_receiver_simulator import run_ir_receiver_simulator
from simulators.msw_simulator import simulate_membrane_switch


class IRReceiverController(Controller):
    def __init__(self, pi_id, component_id, settings, threads, ir_callback):
        super().__init__(pi_id, component_id, settings, threads)
        self.ir_callback = ir_callback

    def callback(self, command):
        self.publish_measurements([('Command', command)])
        self.ir_callback(command)

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=run_ir_receiver_simulator, args=(2, self.callback, self.stop_event))
        else:
            from sensors.ir_receiver import IrReceiver, run_ir_receiver_loop
            ir_receiver = IrReceiver(self.component_id, self.settings['pin'])
            thread = threading.Thread(target=run_ir_receiver_loop, args=(ir_receiver, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
