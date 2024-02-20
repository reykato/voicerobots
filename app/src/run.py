from videostream import VideoStream

HOST_IP = "104.236.9.181"
VIDEO_HOST_PORT = 5005
CAMERA_ADDRESS = 0


def main():
    vs = VideoStream(HOST_IP, VIDEO_HOST_PORT, 30, CAMERA_ADDRESS)
    vs.start()
    input("Stream started. Press ENTER to stop.")
    vs.stop()

if __name__ == '__main__':
    main()
