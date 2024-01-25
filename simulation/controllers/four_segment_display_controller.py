import threading
import time

from controllers.controller import Controller
from system_logic.alarm_clock import AlarmClock
from utility.safe_print import SafePrint


class FourSegmentDisplayController(Controller):
    def __init__(self, pi_id, component_id, settings, threads):
        super().__init__(pi_id, component_id, settings, threads)

        self.simulated = settings.get('simulated', False)
        if not self.simulated:
            from actuators.four_segment_display import FourSegmentDisplay
            self.segment_display = FourSegmentDisplay(component_id, settings['seg_p'], settings['dig_p'])
        else:
            self.segment_display = None

    def callback(self, first_digit, second_digit, third_digit, fourth_digit):
        if AlarmClock.is_alarm_active():
            SafePrint.print("B4SD is blinking.")

        self.publish_measurements([('Time', f"{first_digit}{second_digit}:{third_digit}{fourth_digit}")])

    def show_time(self):
        while not self.stop_event.is_set():
            time.sleep(1)
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)

            if not self.simulated:
                self.segment_display.display_time(s)

            self.callback(s[0], s[1], s[2], s[3])

    def run_loop(self):
        thread = threading.Thread(target=self.show_time, args=())
        thread.start()
        self.threads.append(thread)
