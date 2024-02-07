#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'




def run():
    lidar = RPLidar(PORT_NAME)


    for i, scan in enumerate(lidar.iter_scans()):
        print('%d: Got %d measurments' % (i, len(scan)))
        for s in scan:
            print(s)
        if i > 10:
            break

    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()