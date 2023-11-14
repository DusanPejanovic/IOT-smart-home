import time


class Controller:
    def __init__(self, pi_id, component_id, settings, threads, console_lock, stop_event):
        self.pi_id = pi_id
        self.component_id = component_id
        self.settings = settings
        self.console_lock = console_lock
        self.threads = threads
        self.stop_event = stop_event

    def get_basic_info(self):
        t = time.localtime()
        basic_info = "*" * 20 + "\n"
        basic_info += f"Pi id: {self.pi_id}\n"
        basic_info += f"Component_id: {self.component_id}\n"
        basic_info += f"Timestamp: {time.strftime('%H:%M:%S', t)}"
        return basic_info

    def callback(self, *args):
        raise NotImplementedError("Subclasses must implement this method")

    def run_loop(self):
        raise NotImplementedError("Subclasses must implement this method")
