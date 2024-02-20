from videostream import VideoStream
from controlstreamhandler import ControlStreamHandler

HOST_IP = "104.236.9.181"
VIDEO_HOST_PORT = 5005
CONTROL_HOST_PORT = 5006
CAMERA_ADDRESS = 0

vs = VideoStream(HOST_IP, VIDEO_HOST_PORT, 15, CAMERA_ADDRESS)
csh = ControlStreamHandler(HOST_IP, CONTROL_HOST_PORT)
def main():
    vs.start()
    csh.start()
    input("Stream started. Press ENTER to stop.")
    csh.stop()
    vs.stop()

if __name__ == '__main__':
    main()
