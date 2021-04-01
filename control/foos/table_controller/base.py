from foos.control import Control
from typing import Tuple
from foos.state import State, StateHistory
from foos.display import Display
from foos.frame_processing.ball_detect import get_ball_pos

class TableController:
  def __init__(self):
    self.states: StateHistory = StateHistory()
    self.control = Control()
    self.display = Display()

  def run(self) -> bool:
    if not self.read():
      return False

    motion_target = self.process_state()
    self.display.show(self.states, motion_target)

    #self.drive(motion_target)
    return True

  def process_frame(self, frame, frame_id) -> bool:
    state = State()
    state.frame = frame
    state.frame_id = frame_id
    get_ball_pos(state)
    self.states.update(state)
    return True

  def process_state(self):
    return self.control.process(self.states)