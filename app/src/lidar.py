'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
# import RPi.GPIO as GPIO
import queue
import random
from flask import Flask, render_template, Response

PORT_NAME = '/dev/ttyS0'
DMAX = 2000
IMIN = 0
IMAX = 50

q = queue.Queue()

flask_instance = Flask(__name__)

@flask_instance.route('/')
def index():
    return render_template('index.html')

def main():
    # lidar = RPLidar(PORT_NAME)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(8, GPIO.OUT)
    # motor = GPIO.PWM(8, 1000)
    # motor.start(100)

    # for i, scan in enumerate(lidar.iter_scans()):
    #     print('%d: Got %d measurments' % (i, len(scan)))
    #     for s in scan:
    #         print(s)

    plt.figure()
    ax = plt.subplot(projection='polar')

    for _ in range(200):
        tuple = (random.uniform(0.15,0.3), random.uniform(0,359.9), random.uniform(100, 8000))
        q.put(tuple)
    scan = []
    while not q.empty():
        scan.append(q.get())

    x = [point[2] * np.cos(np.radians(point[1])) for point in scan]
    y = [point[2] * np.sin(np.radians(point[1])) for point in scan]
    color = ["white" for _ in scan]
    plt.scatter(x, y, s=5, c=color, lw=0)

    ax.set_ylim(0, 8000)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("black")

    # ax.set_rmax(DMAX)
    # ax.grid(True)

    # iterator = lidar.iter_scans()

    # ani = animation.FuncAnimation(fig, update_line, fargs=(q, line), interval=40, cache_frame_data=False)
    plt.show()

    # motor.ChangeDutyCycle(0)
    
    # lidar.stop()
    # lidar.disconnect()


if __name__ == '__main__':
    main()