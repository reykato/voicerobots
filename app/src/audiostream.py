import speech_recognition as sr
import time
import socket
from queue import Queue
from stream import Stream
from time import sleep
import math
import pickle

class AudioStream(Stream):
    MAX_PACKET_SIZE = 65000

    def __init__(self, host:str, port:int):
        super().__init__(host, port)
        self.socket = None
        self.audio = sr.Recognizer()
        # self.audio.energy_threshold = 1000
        # self.audio.dynamic_energy_threshold = False
        self.source = sr.Microphone(sample_rate=16000)
        self.buffer = Queue()

    def _handle_stream(self):
        while not self.stop_event.is_set():
            if not self.buffer.empty():
                    print("collected audio")
                    audiodata = b''.join(self.buffer.queue)
                    self.buffer.queue.clear()

                    datasize = len(audiodata)

                    num_of_packets = 1
                    if datasize > self.MAX_PACKET_SIZE:
                        num_of_packets = math.ceil(datasize/self.MAX_PACKET_SIZE)

                    frame_info = {"packs":num_of_packets}
                    # send the number of packs to be expected
                    self.socket.sendto(pickle.dumps(frame_info), (self.host, self.port))

                    left = 0
                    right = self.MAX_PACKET_SIZE

                    for _ in range(num_of_packets):
                        # truncate data to send
                        data = audiodata[left:right]
                        left = right
                        right += self.MAX_PACKET_SIZE

                        # send the frames accordingly
                        self.socket.sendto(data, (self.host, self.port))
            else:
                sleep(0.25)

    def _before_starting(self):
        self.prev_time = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.2)
        with self.source:
            self.audio.adjust_for_ambient_noise(self.source)

        def cb(_, a:sr.AudioData):
            data = a.get_raw_data()
            self.buffer.put(data)
        self.audio.listen_in_background(self.source, cb, phrase_time_limit=5)
        
    def _after_stopping(self):
        self.socket.close()