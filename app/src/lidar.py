#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import RPi.GPIO as GPIO

PORT_NAME = '/dev/ttyS0'
DMAX = 2000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    GPIO.setmode(GPIO.BCM)
    motor = GPIO.PWM(8, 1000)
    motor.start(100)

    # for i, scan in enumerate(lidar.iter_scans()):
    #     print('%d: Got %d measurments' % (i, len(scan)))
    #     for s in scan:
    #         print(s)

    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=200)
    plt.show()

    motor.ChangeDutyCycle(0)
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()