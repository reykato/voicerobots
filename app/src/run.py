from videostream import VideoStream
from controlstreamhandler import ControlStreamHandler
from audiostream import AudioStream

HOST_IP = "104.236.9.181"
VIDEO_HOST_PORT = 5005
CONTROL_HOST_PORT = 5006
AUDIO_HOST_PORT = 5007
CAMERA_ADDRESS = 0
vs = VideoStream(HOST_IP, VIDEO_HOST_PORT, 15, CAMERA_ADDRESS)
csh = ControlStreamHandler(HOST_IP, CONTROL_HOST_PORT)
# aus = AudioStream(HOST_IP, AUDIO_HOST_PORT)
def main():
    vs.start()
    csh.start()
    # aus.start()
    input("Stream started. Press ENTER to stop.")
    csh.stop()
    vs.stop()
    # aus.stop()

if __name__ == '__main__':
    main()
