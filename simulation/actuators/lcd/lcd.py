from datetime import datetime

from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO


class LCD:
    def __init__(self, id, pin_rs=0, pin_e=2, pins_db=None):
        self.id = id
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.

        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db if pins_db is not None else [4, 5, 6, 7]

        # Create PCF8574 GPIO adapter.
        addresses = [self.PCF8574_address, self.PCF8574A_address]
        for address in addresses:
            try:
                self.mcp = PCF8574_GPIO(address)
                break
            except Exception as e:
                print(f'I2C Address Error at {address}: {e}')
        else:
            print('No valid I2C address found for LCD.')
            return

        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=self.pin_rs, pin_e=self.pin_e, pins_db=self.pins_db, GPIO=self.mcp)

    def get_time_now(self):
        return datetime.now().strftime('    %H:%M:%S')

    def display_time(self):
        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(16, 2)  # set number of LCD lines and columns

        self.lcd.setCursor(0, 0)  # set cursor position
        self.lcd.message('Current time:\n')
        self.lcd.message(self.get_time_now())

    def display_password_message(self):
        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(16, 2)  # set number of LCD lines and columns

        self.lcd.setCursor(0, 0)  # set cursor position
        self.lcd.message('Enter the password for a garage.')

    def display_dht_values(self, temperature, humidity):
        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(16, 2)  # set number of LCD lines and columns

        self.lcd.setCursor(0, 0)  # set cursor position
        self.lcd.message("Temperature: {}\n".format(temperature))
        self.lcd.message("Humidity: {}".format(humidity))

    def destroy(self):
        self.lcd.clear()

# def run_lcd_loop(lcd, delay, callback, stop_event):
#     while not stop_event.is_set():
#         sleep(delay)
#         if random.random() < 0.5:
#             lcd.display_time()
#             text = "Enter the password for a garage."
#             callback(text)
#         else:
#             lcd.display_password_message()
#             text = 'Current time:\n' + lcd.get_time_now()
#             callback(text)
#
#     lcd.destroy()
