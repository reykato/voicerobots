import pickle
import math
import socket
import cv2

class VideoStream():
    MAX_PACKET_SIZE = 65000

    def __init__(host, port, camera_address=0):
        HOST = host
        PORT = port
        CAMERA_ADDRESS = camera_address
    
    def handle_video_stream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        cap = cv2.VideoCapture(self.CAMERA_ADDRESS)
        ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

        # get frame from camera
        ret, frame = cap.read()

        while ret:
            # compress frame to jpg with 80% quality
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            retval, buffer = cv2.imencode('.jpg', frame, encode_param)

            if retval:
                buffer = buffer.tobytes() # convert to byte array
                buffer_size = len(buffer) # get size of the frame

                num_of_packets = 1
                if buffer_size > self.MAX_PACKET_SIZE:
                    num_of_packets = math.ceil(buffer_size/self.MAX_PACKET_SIZE)

                frame_info = {"packs":num_of_packets}

                # send the number of packs to be expected
                print("Number of packs:", num_of_packets)
                sock.sendto(pickle.dumps(frame_info), (self.HOST_IP, self.VIDEO_HOST_PORT))
                
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
                    sock.sendto(data, (self.HOST_IP, self.VIDEO_HOST_PORT))
            ret, frame = cap.read()
