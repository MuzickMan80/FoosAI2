# Write your code here :-)
import time
from fps import FPS
from webcam import WebcamVideoStream

cam = WebcamVideoStream(0,resolution=(352,288),fps=30).start()
time.sleep(2.0)

fps = FPS().start()

def get_frame():
    return cam.read()

if __name__ == "__main__":
    while true:
        frame = get_frame()