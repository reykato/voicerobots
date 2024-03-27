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
                        print(f"Received control: {decoded_data}")
                        x = decoded_data[0]
                        y = decoded_data[1]
                        self.motors.set_stepper_speed(x, y)
                    else:
                        self._connect_to_server()
            except socket.error as e:
                received_data = None
                if not e.args[0] == 'timed out':
                    print(f"Error: '{e.args[0]}', reconnecting...")
                    self._connect_to_server()

    def _connect_to_server(self):
        while True:
            try:
                print("Trying to connect to server...")
                self.socket.connect((self.host, self.port))
                break  # Exit the loop if connection succeeds
            except socket.error:
                print("Failed to connect, retrying in 1 second...")
                time.sleep(1)  # Wait for 1 second before trying again
            except KeyboardInterrupt:
                print("Connection attempt cancelled.")
                self._after_stopping()
                break

    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_to_server()
        self.socket.settimeout(0.2)

    def _after_stopping(self):
        self.socket.close()
        self.motors.cleanup()
