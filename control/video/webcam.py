# import the necessary packages
from threading import Thread, Lock
import time
import cv2

class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream", resolution=None, fps=None):
        #initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)

        if resolution:
            w,h = resolution
            self.stream.set(3,w)
            self.stream.set(4,h)
        if fps:
            self.stream.set(5,fps)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        self.frame_index = 0
        self.last_read = None

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            self.frame_index = self.frame_index + 1

    def read(self):
        # return the frame most recently read
        while self.last_read == self.frame_index:
            time.sleep(0.001);

        self.last_read = self.frame_index
        return (self.grabbed, self.frame)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True