import threading

from controllers.controller import Controller
from simulators.lcd_simulator import simulate_lcd


class LCDController(Controller):
    def callback(self, text, verbose=False):
        self.publish_measurements([('Text', text)])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_lcd, args=(2, self.callback, self.stop_event))
        else:
            from actuators.lcd import LCD, run_lcd_loop
            lcd = LCD(self.component_id, self.settings['pin_rs'], self.settings['pin_e'], self.settings['pins_db'])
            thread = threading.Thread(target=run_lcd_loop, args=(lcd, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
