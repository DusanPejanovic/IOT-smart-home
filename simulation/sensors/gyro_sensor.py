import time
import os


def run_gyro_loop(mpu, delay, callback, stop_event):
    while not stop_event.is_set():
        time.sleep(delay)
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()
        os.system('clear')

        accel = [round(value / 16384.0, 2) for value in accel]
        gyro = [round(value / 131.0, 2) for value in gyro]

        callback(accel, gyro)
