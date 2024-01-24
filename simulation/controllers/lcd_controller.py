from controllers.controller import Controller


class LCDController(Controller):
    def __init__(self, pi_id, component_id, settings, threads):
        super().__init__(pi_id, component_id, settings, threads)

        self.simulated = settings.get('simulated', False)
        if not self.simulated:
            from actuators.lcd.lcd import LCD
            self.lcd = LCD(component_id, settings['pin_rs'], settings['pin_e'], settings['pins_db'])
        else:
            self.lcd = None

    def callback(self, text):
        self.publish_measurements([('Text', text)])

    def display_dht_values(self, temperature, humidity):
        if not self.simulated:
            self.lcd.display_dht_values(temperature, humidity)

        self.callback(f"Temperature : {temperature}, Humidity: {humidity}")

    def run_loop(self):
        pass
