import pickle
import math
import socket
import time
import threading
import cv2
from stream import Stream

class VideoStream(Stream):
    MAX_PACKET_SIZE = 65000

    def __init__(self, host:str, port:int, fps:int, camera_address=0):
        super.__init__()
        self.FPS = fps
        self.CAMERA_ADDRESS = camera_address

        self.socket = None
        self.capture = cv2.VideoCapture(self.CAMERA_ADDRESS)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.prev_time = 0

    def _handle_stream(self):
        while not self.stop_event.is_set():
            # get frame from camera
            time_elapsed = time.time() - self.prev_time
            ret, frame = self.capture.read()

            # if enough time has passed between the last frame and now
            if time_elapsed > 1./self.FPS:
                self.prev_time = time.time()

                # if the VideoCapture.read() function says the read was successful, continue and send frame
                if ret:
                    # compress frame to jpg with 80% quality
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    retval, buffer = cv2.imencode('.jpg', frame, encode_param)

                    # if retval:
                    buffer = buffer.tobytes() # convert to byte array
                    buffer_size = len(buffer) # get size of the frame

                    num_of_packets = 1
                    if buffer_size > self.MAX_PACKET_SIZE:
                        num_of_packets = math.ceil(buffer_size/self.MAX_PACKET_SIZE)

                    frame_info = {"packs":num_of_packets}

                    # send the number of packs to be expected
                    print("Number of packs:", num_of_packets)
                    self.socket.sendto(pickle.dumps(frame_info), (self.HOST, self.PORT))
                    
                    left = 0
                    right = self.MAX_PACKET_SIZE

                    for i in range(num_of_packets):
                        # print("left:", left)
                        # print("right:", right)

                        # truncate data to send
                        data = buffer[left:right]
                        left = right
                        right += self.MAX_PACKET_SIZE

                        # send the frames accordingly
                        self.socket.sendto(data, (self.HOST, self.PORT))
            ret, frame = self.capture.read()

    def _before_starting(self):
        self.prev_time = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _after_stopping(self):
        self.socket.close()
        