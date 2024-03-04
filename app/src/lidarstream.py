import socket
from stream import Stream
import RPi.GPIO as GPIO
from rplidar import RPLidar
import numpy as np

class LidarStream(Stream):
    PORT_NAME = '/dev/ttyS0'
    MOTOR_PIN = 18

    def __init__(self, host, port):
        super().__init__(host, port)

    def _handle_stream(self):
        while not self.stop_event.is_set():
            scan = next(self.iterator)
            data = []
            for point in scan:
                data += scan
            print(f"sending {data}...")
            np_data = np.array(data, dtype=np.float32)
            byte_buffer = np_data.tobytes()
            self.socket.sendto(byte_buffer, (self.host, self.port))

    def _before_starting(self):
        self.actual_fps = 0
        self.time_elapsed_second = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._connect_to_server()

        self.lidar = RPLidar(self.PORT_NAME)
        self.iterator = self.lidar.iter_scans()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR_PIN, GPIO.OUT)
        self.motor = GPIO.PWM(self.MOTOR_PIN, 1000)
        self.motor.start(100)

    def _after_stopping(self):
        self.socket.close()