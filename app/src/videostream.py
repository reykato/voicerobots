import pickle
import math
import socket
import time
import cv2
from stream import Stream

class VideoStream(Stream):
    MAX_PACKET_SIZE = 65000

    def __init__(self, host:str, port:int, fps:int, camera_address=0):
        super().__init__(host, port)
        self.fps = fps
        self.camera_address = camera_address

        self.socket = None
        self.capture = cv2.VideoCapture(self.camera_address)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
        self.capture.set(cv2.CAP_PROP_FPS, fps)
        self.prev_time = 0
        self.actual_fps = 0
        self.time_elapsed_second = 0

    def _handle_stream(self):
        while not self.stop_event.is_set():
            # get frame from camera
            time_elapsed = time.time() - self.prev_time
            # ret, frame = self.capture.read()

            if time.time() - self.time_elapsed_second > 1:
                print(f"Calculated FPS: {self.actual_fps}")
                self.actual_fps = 0
                self.time_elapsed_second = time.time()

            # if enough time has passed between the last frame and now
            if time_elapsed > 1./self.fps:
                self.prev_time = time.time()
                self.actual_fps += 1

                ret, frame = self.capture.read()

                # if the VideoCapture.read() function says the read was successful, continue and send frame
                if ret:
                    # compress frame to jpg with 80% quality
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    _, buffer = cv2.imencode('.jpg', frame, encode_param)

                    # if retval:
                    buffer = buffer.tobytes() # convert to byte array
                    buffer_size = len(buffer) # get size of the frame

                    num_of_packets = 1
                    if buffer_size > self.MAX_PACKET_SIZE:
                        num_of_packets = math.ceil(buffer_size/self.MAX_PACKET_SIZE)

                    frame_info = {"packs":num_of_packets}

                    # send the number of packs to be expected
                    # print("Number of packs:", num_of_packets)
                    self.socket.sendto(pickle.dumps(frame_info), (self.host, self.port))

                    left = 0
                    right = self.MAX_PACKET_SIZE

                    for _ in range(num_of_packets):
                        # truncate data to send
                        data = buffer[left:right]
                        left = right
                        right += self.MAX_PACKET_SIZE

                        # send the frames accordingly
                        self.socket.sendto(data, (self.host, self.port))

    def _before_starting(self):
        self.actual_fps = 0
        self.time_elapsed_second = 0
        self.prev_time = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _after_stopping(self):
        self.socket.close()
