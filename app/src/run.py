from videostream import VideoStream

HOST_IP = "104.236.9.181"
VIDEO_HOST_PORT = 5005
CAMERA_ADDRESS = 0

vs = VideoStream(HOST_IP, VIDEO_HOST_PORT, CAMERA_ADDRESS)

def main():
    vs.handle_video_stream()

if __name__ == '__main__':
    main()