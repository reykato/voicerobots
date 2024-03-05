import socket
from stream import Stream
import RPi.GPIO as GPIO
from rplidar import RPLidar
import numpy as np
import time

class LidarStream(Stream):
    PORT_NAME = '/dev/ttyS0'
    MOTOR_PIN = 18

    def _handle_stream(self):
        while not self.stop_event.is_set():
            scan = None
            try:
                scan = next(self.iterator)
            except:
                self._after_stopping()
                self._before_starting()
            
            # print(f"sending data...")
            np_data = np.array(scan, dtype=np.float32)
            byte_buffer = np_data.tobytes()

            self.socket.sendto(byte_buffer, (self.host, self.port))
            time.sleep(0.1)


    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._connect_to_server()
        self.lidar = RPLidar(self.PORT_NAME)
        
        self.iterator = self.lidar.iter_scans()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR_PIN, GPIO.OUT)
        self.motor = GPIO.PWM(self.MOTOR_PIN, 1000)
        self.motor.start(100)

    def _after_stopping(self):
        self.lidar.stop()
        GPIO.cleanup()
        self.socket.close()