from streamhandler import StreamHandler
import socket
import struct
from motors import Motors

class ControlStreamHandler(StreamHandler):
    socket = None

    motors = Motors(20, 21, 16, 12, 1, 7) # initialize motors with GPIO pin numbers

    def _handle_stream(self):
        while not self.stop_event.is_set():
            try:
                received_data = self.socket.recv(1024)
            except socket.error as e:
                received_data = None
                if not e.args[0] == 'timed out':
                    print(err = e.args[0])
                    self.stop()

            if not received_data is None:
                decoded_data = struct.unpack('2d', received_data)
                print(f"Received: {decoded_data}")

                # Echo back the received data
                self.socket.sendto(decoded_data, (self.host, self.port))
                self.motors.set_duty_cycle(decoded_data[0], decoded_data[1])

    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.socket.connect((self.host, self.port))
                break  # Exit the loop if connection succeeds
            except socket.error as e:
                print(f"Failed to connect: {e}, retrying...")
                # time.sleep(1)  # Wait for 1 second before trying again
    
    def _after_stopping(self):
        self.socket.close()