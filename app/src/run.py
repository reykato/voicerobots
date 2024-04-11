from videostream import VideoStream
from controlstream import ControlStream
from audiostream import AudioStream
from lidarstream import LidarStream

# HOST_IP = "159.65.162.35"
HOST_IP = "10.20.9.254"
VIDEO_HOST_PORT = 5005
CONTROL_HOST_PORT = 5006
AUDIO_HOST_PORT = 5007
LIDAR_HOST_PORT = 5008

CAMERA_ADDRESS = 0

vs = VideoStream(HOST_IP, VIDEO_HOST_PORT, 10, CAMERA_ADDRESS)
csh = ControlStream(HOST_IP, CONTROL_HOST_PORT)
aus = AudioStream(HOST_IP, AUDIO_HOST_PORT)
ls = LidarStream(HOST_IP, LIDAR_HOST_PORT)

def main():
    vs.start()
    csh.start()
    aus.start()
    ls.start()
    input("Stream started. Press ENTER to stop.")
    csh.stop()
    vs.stop()
    aus.stop()
    ls.stop()

if __name__ == '__main__':
    try:
        main()
    except:
        csh.stop()
        vs.stop()
        vs.stop()
        ls.stop()
