import os

import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from utils.usb6008 import USB6008
from utils.mqtt import MQTT

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def lowpass_filter(x, y_prev, Tf, Ts):
    a = Tf / (Tf + Ts)
    return a * x + (1 - a) * y_prev


if __name__ == '__main__':
    # USB6008 setup
    usb6008 = USB6008()

    # MQTT setup
    load_dotenv()
    mqtt = MQTT("IOT3", os.getenv("MQTT_BROKER_URL"), int(os.getenv("MQTT_BROKER_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))

    # Environnement parameters
    Tenv = 21.5

    # Control parameters
    Ts = 0.1  # Sample time [s]
    Tstop = 100  # Simulation time [s]
    N = int(Tstop / Ts)  # Number of samples

    # Controller parameters (from stability_analysis.py)
    Kp = 1.84
    Ti = 19.75

    # Control setup
    r = 25  # Reference temperature [degC]
    e = np.zeros(N + 1)  # Error [degC]
    u = np.zeros(N + 1)  # Control signal [V]
    Tout = np.zeros(N + 2)  # Output temperature [degC]
    Tout[0] = Tenv  # Initial output temperature [degC]
    Tf = 0.5  # Lowpass Filter time constant [s]
    t = np.arange(0, Tstop + 2 * Ts, Ts)  # Time vector [s]

    # Plot setup
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(311)
    line1, = ax.plot(t, Tout, '+-')
    ax.set_xlabel('Time [s]')
    ax.set_xlim([0, Tstop])
    ax.set_ylabel('Output temperature [degC]')
    ax.set_ylim([0, 35])
    ax.grid()
    ax = fig.add_subplot(312)
    line2, = ax.plot(t[:-1], e)
    ax.set_xlabel('Time [s]')
    ax.set_xlim([0, Tstop])
    ax.set_ylabel('Error [degC]')
    ax.set_ylim([-5, 5])
    ax.grid()
    ax = fig.add_subplot(313)
    line3, = ax.plot(t[:-1], u)
    ax.set_xlabel('Time [s]')
    ax.set_xlim([0, Tstop])
    ax.set_ylabel('Control signal [V]')
    ax.set_ylim([0, 5])
    ax.grid()

    # Simulation
    for k in range(N + 1):
        # Error
        e[k] = r - Tout[k]

        # Control signal
        u[k] = u[k - 1] + Kp * (e[k] - e[k - 1]) + Kp / Ti * e[k]
        u[k] = min(max(u[k], 0), 5)

        # Output control signal
        usb6008.write(u[k])

        # Read temperature
        ToutVolt = usb6008.read()
        ToutVolt = min(max(ToutVolt, 1), 5)
        ToutDegC = map_range(ToutVolt, 1, 5, 0, 50)
        Tout[k + 1] = lowpass_filter(ToutDegC, Tout[k], Tf, Ts)

        # Publish temperature
        mqtt.publish("temperature", Tout[k + 1])

        # Update plot
        line1.set_data(t[:k], Tout[:k])
        line2.set_data(t[:k], e[:k])
        line3.set_data(t[:k], u[:k])
        fig.canvas.draw()
        plt.pause(Ts)

    plt.ioff()
    usb6008.close()
    plt.show()
