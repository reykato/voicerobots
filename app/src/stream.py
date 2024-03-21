import threading
import time
import socket

class Stream():
    """
    Class for streaming data via IP.

    Parameters:
    - host (str): Address of the receiving machine.
    (e.g. "70.224.3.88")
    - port (int): Port which the receiving machine is listening to.
    (e.g. 5100)
    """
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None

        self.stop_event = threading.Event()
        self.loop_thread = threading.Thread(target=self._handle_stream)

    def _handle_stream(self):
        """
        Processes data into packets and sends them to
        the receiving machine. Should contain a loop.
        """
        pass

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
                break

    def _after_stopping(self):
        """
        Code to execute after stopping the loop `_handle_stream`.
        """
        pass
    def _before_starting(self):
        """
        Code to execute before starting the loop `_handle_stream`.
        """   
        pass
    def start(self):
        """
        Executes code in `_before_starting`, then opens thread on
        `_handle_stream`.
        """

        if not self.loop_thread.is_alive():
            self._before_starting()
            self.stop_event.clear()
            self.loop_thread = threading.Thread(target=self._handle_stream)
            self.loop_thread.start()
            print("Loop started.")
        else:
            print("Loop is already running.")

    def stop(self):
        """
        Stops the loop started using `start()` and runs code at `_after_stopping`.
        """
   
        if self.loop_thread.is_alive():
            self.stop_event.set()
            self.loop_thread.join()
            self._after_stopping()
            print("Loop stopped.")
        else:
            print("Loop is not running.")
    