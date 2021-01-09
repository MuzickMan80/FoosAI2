from .base import TableController
from video.file import FileVideoStream
import pathlib
import time
import cv2

def nothing(x):
  pass

class SimTableController(TableController):
  def __init__(self):
    basepath = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
    self.video = FileVideoStream(basepath.joinpath("data/videos/table_angled_processed.mp4").absolute())
    TableController.__init__(self)
    self.paused = False

    cv2.namedWindow("Playback")
    cv2.createTrackbar("Pause", "Playback", 0, 1, nothing)
    cv2.createTrackbar("Pos", "Playback", 0, int(self.video.frame_count-1), nothing)
    cv2.createTrackbar("Speed", "Playback", 0, 5, nothing)
    cv2.setTrackbarPos("Speed", "Playback", 1)

  def read(self) -> bool:
    frame_id = cv2.getTrackbarPos("Pos", "Playback")
    paused = cv2.getTrackbarPos("Pause", "Playback") == 1
    speed = cv2.getTrackbarPos("Speed", "Playback")

    # skip 0 to 1000 (due to moved paper)
    if frame_id < 1000:
      frame_id = 1000

    # skip 4300 to 8000 (due to moved paper)
    if frame_id >= 4300 and frame_id < 8000:
      frame_id = 8000

    if not paused:
      frame_id = frame_id + 1

    self.video.seek(frame_id)
    time.sleep(speed*0.025)
    
    grabbed,frame = self.video.read()
    if not grabbed:
      return False

    cv2.setTrackbarPos("Pos", "Playback", frame_id)
    return self.process_frame(frame, frame_id)


