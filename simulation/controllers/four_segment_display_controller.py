import threading

from controllers.controller import Controller
from simulators.four_segment_display_simulator import simulate_four_segment_display


class FourSegmentDisplayController(Controller):
    def callback(self, first_digit, second_digit, third_digit, fourth_digit, verbose=False):
        self.publish_measurements([('Digits', f"{first_digit}{second_digit}:{third_digit}{fourth_digit}")])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_four_segment_display, args=(self.callback, self.stop_event))
        else:
            from actuators.four_segment_display import FourSegmentDisplay, show_time_on_four_segment_display
            four_segment_display = FourSegmentDisplay(self, self.settings["seg_pins"], self.settings["dig_pins"])
            thread = threading.Thread(target=show_time_on_four_segment_display,
                                      args=(four_segment_display, 2, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
