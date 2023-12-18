from controllers.buzzer_controller import BuzzerController
from controllers.led_controller import LedController
from settings import load_settings


def read_led_diodes_and_buzzers():
    led_diodes = []
    buzzers = []

    settings = load_settings()
    for pi_id, pi_settings in settings.items():
        for device_id, device_settings in pi_settings.items():
            if device_settings["type"] == "LED":
                if device_settings["simulated"]:
                    led_diodes.append(LedController(pi_id, device_id, device_settings["simulated"]))
                else:
                    led_diodes.append(LedController(pi_id, device_id, device_settings["simulated"], device_settings["pin"]))
            elif device_settings["type"] == "BZR":
                if device_settings["simulated"]:
                    buzzers.append(BuzzerController(pi_id, device_id, device_settings["simulated"]))
                else:
                    buzzers.append(BuzzerController(pi_id, device_id, device_settings["simulated"], device_settings["pin"]))
    return led_diodes, buzzers


def clear_terminal(header):
    print()
    print("*" * 20 + " " + header + " " + "*" * 20)


def diodes_management(led_diodes):
    while True:
        clear_terminal("Led diode management")
        for i in range(0, len(led_diodes)):
            diode = led_diodes[i]
            print(diode.pi_id + ", " + diode.name + " -> " + str(i))

        command = input("Select diode to toggle: ")
        if command == "x":
            break
        elif command.isdigit() and 0 <= int(command) < len(led_diodes):
            led_diodes[int(command)].change_led_state()


def buzzer_management(buzzers):
    while True:
        clear_terminal("Buzzer management")
        for i in range(0, len(buzzers)):
            buzzer = buzzers[i]
            print(buzzer.pi_id + ", " + buzzer.name + " -> " + str(i))

        command = input("Select buzzer to toggle: ")
        if command == "x":
            break
        elif command.isdigit() and 0 <= int(command) < len(buzzers):
            buzzers[int(command)].change_buzzer_state()


if __name__ == '__main__':
    led_diodes, buzzers = read_led_diodes_and_buzzers()
    while True:
        clear_terminal("Menu")
        print("Led diodes management -> 0")
        print("Buzzer management -> 1")
        command = input("Enter the command: ")
        if command == "x":
            break

        if command == "0":
            if len(led_diodes) == 0:
                print("There are no led diodes connected.")
            else:
                diodes_management(led_diodes)
        if command == "1":
            if len(buzzers) == 0:
                print("There are no buzzers connected.")
            else:
                buzzer_management(buzzers)
