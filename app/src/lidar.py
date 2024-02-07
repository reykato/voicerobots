from pyrplidar import PyRPlidar
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

DMAX = 4000
IMIN = 0
IMAX = 50

def simple_express_scan():

    
    
    
    
    for count, scan in enumerate(scan_generator()):
        print(count, scan)
        if count == 20: break

    lidar.stop()

    
    lidar.disconnect()

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
    scan_generator = lidar.start_scan_express(4)
                  
    lidar.set_motor_pwm(500)
    time.sleep(2)

    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    # iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(scan_generator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()


if __name__ == "__main__":
    run()