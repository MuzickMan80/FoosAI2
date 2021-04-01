from typing import List
from enum import IntEnum, Enum

class ObjAccuracy(IntEnum):
    NotFound = 0
    Found = 1
    Predicted = 2
    LastKnown = 3

class Position:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.accuracy = ObjAccuracy.NotFound
    def valid(self):
        return self.x != None and self.y != None
    def get(self):
        return (self.x, self.y)
    def set_pos(self, x, y, accuracy=ObjAccuracy.Found):
        self.x = x
        self.y = y
        self.accuracy = accuracy
    
class RodPosition:
    def __init__(self):
        self.pos = 0.5
        self.accuracy = ObjAccuracy.NotFound
    def set_pos(self, pos, accuracy=ObjAccuracy.Found):
        if pos < 0:
            pos = 0
        if pos > 1:
            pos = 1
        self.pos = pos
        self.accuracy = accuracy
    def get_pos(self):
        return self.__pos
    
class PlayerState:
    def __init__(self):
        self.goalie = RodPosition()
        self.twoman = RodPosition()
        self.fiveman = RodPosition()
        self.threeman = RodPosition()

class MotionControlMode(IntEnum):
    Coast = 0
    Position = 1
    Velocity = 2
    Brake = 3

class MotionControlAxis:
    def __init__(self):
        self.mode = MotionControlMode.Coast
        self.target = 0

class PlayerControlRod:
    def __init__(self):
        self.rotation = MotionControlAxis()
        self.translation = MotionControlAxis()

class PlayerControl:
    def __init__(self):
        self.goalie = PlayerControlRod()
        self.twoman = PlayerControlRod()
        self.fiveman = PlayerControlRod()
        self.threeman = PlayerControlRod()

class State:
    def __init__(self):
        self.player = PlayerState()
        self.opponent = PlayerState()
        self.ball = Position()
        self.frame = None
        self.frame_id = 0
        self.layers = {}
        self.control = PlayerControl()

class StateHistory:
    def __init__(self):
        self.state0 = State()
        self.state1 = State()
        self.state2 = State()

    def update(self, state: State):
        if not type(state) == State:
            raise Exception("Invalid state: " + str(state))

        self.state2 = self.state1
        self.state1 = self.state0
        self.state0 = state
    
    def latest() -> State:
        return self.state0

    def all() -> List[State]:
        return [self.state0, self.state1, self.state2]