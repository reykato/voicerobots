import socket
import time
import numpy as np
from motors import Motors
from streamhandler import StreamHandler

class ControlStreamHandler(StreamHandler):
    socket = None
    motors = Motors(20, 21, 12, 16, 1, 7) # initialize motors with GPIO pin numbers

    def _handle_stream(self):
        while not self.stop_event.is_set():
            try:
                received_data = self.socket.recv(1024)
                if not received_data is None:
                    decoded_data = np.frombuffer(received_data, dtype=np.float32)
                    self.motors.set_stepper_speed(decoded_data[0], decoded_data[1])
            except socket.error as e:
                received_data = None
                if not e.args[0] == 'timed out':
                    print(f"Error: '{e.args[0]}', reconnecting...")
                    self._connect_to_server()

    def _connect_to_server(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
                break  # Exit the loop if connection succeeds
            except socket.error:
                print("Failed to connect, retrying in 1 second...")
                time.sleep(1)  # Wait for 1 second before trying again

    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_to_server()

    def _after_stopping(self):
        self.socket.close()
