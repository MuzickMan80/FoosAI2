import cv2

class FileVideoStream:
    def __init__(self, path):
        self.file = cv2.VideoCapture(str(path))
        self.frame_count = self.file.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_id = 0
        self.frame_ms = 0

    def read(self):        
        self.frame_id = self.file.get(cv2.CAP_PROP_POS_FRAMES)
        self.frame_ms = self.file.get(cv2.CAP_PROP_POS_MSEC)
        return self.file.read()

    def seek(self, frame_id):
        self.file.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
