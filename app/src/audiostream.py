import pyaudio
import time
import socket
from stream import Stream

class AudioStream(Stream):
    MAX_PACKET_SIZE = 65000

    def __init__(self, host:str, port:int):
        super().__init__(host, port)

        self.socket = None
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    def _handle_stream(self):
        while not self.stop_event.is_set():
            try:
                bytes = self.stream.read(1024)
                self.socket.sendto(bytes, (self.host, self.port))
            except IOError:
                pass

    def _before_starting(self):
        self.prev_time = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _after_stopping(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.socket.close()
