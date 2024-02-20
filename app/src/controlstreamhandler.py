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
                if not e.args[0] == errno.EAGAIN and e.args[0] == errno.EWOULDBLOCK:
                    print(err = e.args[0])

            if not received_data == None:
                decoded_data = received_data.decode()
                print(f"Received: {decoded_data}")

                # Echo back the received data
                self.socket.sendall(decoded_data)
                self.motors.set_duty_cycle(decoded_data[0], decoded_data[1])


    
    def _before_starting(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
    
    def _after_stopping(self):
        self.socket.close()