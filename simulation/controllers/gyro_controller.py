import threading

from controllers.controller import Controller
from simulators.gyro_simulator import simulate_gyroscope


class GyroController(Controller):
    def callback(self, acceleration, rotation, verbose=False):
        if verbose:
            with self.console_lock:
                print(self.get_basic_info())
                print(f"Acceleration: {acceleration}")
                print(f"Rotation: {rotation}")

        acc_f = [float(acceleration[0]), float(acceleration[1]), float(acceleration[2])]
        rot_f = [float(rotation[0]), float(rotation[1]), float(rotation[2])]
        self.publish_measurements([('Acceleration', acc_f), ('Rotation', rot_f)])

    def run_loop(self):
        if self.settings['simulated']:
            thread = threading.Thread(target=simulate_gyroscope, args=(self.callback, self.stop_event))
        else:
            from sensors.gyro_sensor import run_gyro_loop
            from sensors.gyroscope.MPU6050 import MPU6050
            mpu = MPU6050()
            mpu.dmp_initialize()
            thread = threading.Thread(target=run_gyro_loop, args=(mpu, 3, self.callback, self.stop_event))

        thread.start()
        self.threads.append(thread)
