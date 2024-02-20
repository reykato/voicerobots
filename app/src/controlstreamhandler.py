from streamhandler import StreamHandler
import socket
import errno
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

            if not received_data == None:
                decoded_data = received_data.decode()
                print(f"Received: {decoded_data}")

                # Echo back the received data
                self.socket.sendall(decoded_data)
                self.motors.set_duty_cycle(decoded_data[0], decoded_data[1])

    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.timeout(0.005) # socket will stop waiting for packets after 5ms
        self.socket.bind((self.host, self.port))
        self.socket.listen()
    
    def _after_stopping(self):
        self.socket.close()