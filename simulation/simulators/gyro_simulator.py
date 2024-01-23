import time
import random


def simulate_gyro_data():
    accel = [random.uniform(-1, 1) for _ in range(3)]
    gyro = [random.uniform(-250, 250) for _ in range(3)]
    return accel, gyro


def simulate_gyroscope(callback, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(1, 5))
        accel, gyro = simulate_gyro_data()

        accel = [round(value, 2) for value in accel]
        gyro = [round(value, 2) for value in gyro]

        callback(accel, gyro)
