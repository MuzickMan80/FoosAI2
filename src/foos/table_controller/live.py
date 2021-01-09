from .base import TableController
from motion import Motion
from video import capture
from state import State

class LiveTableController(TableController):
  def __init__(self):
    super().__init__(self)

  def read_state(self) -> State:
    state = super().read_state(self)
    state.frame = capture.get_frame()
    return state
