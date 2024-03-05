import socket
import time
import numpy as np
from motors import Motors
from stream import Stream

class ControlStream(Stream):
    motors = Motors(20, 21, 12, 16, 7, 1) # initialize motors with GPIO pin numbers

    def _handle_stream(self):
        while not self.stop_event.is_set():
            try:
                received_data = self.socket.recv(1024)
                if not received_data is None:
                    decoded_data = np.frombuffer(received_data, dtype=np.float32)
                    if len(decoded_data) != 0:
                        x = max(min(decoded_data[0], 100), -100)
                        y = max(min(decoded_data[1], 100), -100)
                        self.motors.set_stepper_speed(x, y)
                    else:
                        self._connect_to_server()
            except socket.error as e:
                received_data = None
                if not e.args[0] == 'timed out':
                    print(f"Error: '{e.args[0]}', reconnecting...")
                    self._connect_to_server()

    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_to_server()

    def _after_stopping(self):
        self.motors.cleanup()
        self.socket.close()
