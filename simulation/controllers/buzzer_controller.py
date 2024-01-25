import threading
import time

from MQTT.mqtt_publisher import MQTTPublisher
from controllers.controller import Controller
from system_logic.alarm import Alarm
from system_logic.alarm_clock import AlarmClock

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class BuzzerController(Controller):
    def __init__(self, pi_id, component_id, settings, threads):
        super().__init__(pi_id, component_id, settings, threads)

        self.simulated = settings.get('simulated', False)
        if not self.simulated:
            from actuators.lcd.buzzer import Buzzer
            self.buzzer = Buzzer(component_id, settings['pin'], 1)
        else:
            self.buzzer = None
        self.buzzer_on = False

    def callback(self, buzzer_on):
        self.publish_measurements([("Buzzer", int(buzzer_on))])

    def run_alarm_buzzer(self, stop_event):
        if self.buzzer_on:
            return

        if not self.simulated:
            self.buzzer.turn_on()
        self.callback(True)

        while Alarm.alarm_activated() and not stop_event.is_set():
            time.sleep(0.5)
            if not self.simulated:
                self.buzzer.buzz(0.1)
        if not self.simulated:
            self.buzzer.turn_off()
        self.callback(False)

    def run_alarm_clock_buzzer(self, stop_event):
        if self.buzzer_on:
            return

        if not self.simulated:
            self.buzzer.turn_on()
        self.callback(True)

        while AlarmClock.is_alarm_active() and not stop_event.is_set():
            time.sleep(0.5)
            if not self.simulated:
                self.buzzer.buzz(0.1)
        if not self.simulated:
            self.buzzer.turn_off()
        self.callback(False)

    #TODO
    # def play_song(buzzer, song, song_stop_event, duration=1, pause=1):
    #     for note in song:
    #         if song_stop_event.is_set():
    #             break
    #         buzzer.buzz_note(notes[note['note']], note['duration'] * duration)
    #         if song_stop_event.is_set():
    #             break
    #         time.sleep(note['duration'] * duration * pause)