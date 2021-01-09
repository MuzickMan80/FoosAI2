import cv2
import numpy as np
from math import pi
from typing import Tuple
from foos.state import State, ObjAccuracy

class motion_tracker():
    def __init__(self):
        self.reset()
        self.p = None

    def reset(self):
        self.v = 0
        self.a = 0
        self.valid = False
        self.samples = 0
        self.missing = 0
    
    def calc(self, p, dt=1):
        if self.samples == 0:
            self.p = p
        v = (p-self.p)/dt
        if self.samples == 1:
            self.v = v
        a = (v-self.v)/dt
        if self.samples == 2:
            self.a = a
        j = (a-self.a)/dt
        return (v,a,j)

    def predict(self, dt=1):
        '''
            Predicts the location of the 
        '''
        v = self.v # + self.a*dt
        p = self.p + v*dt
        return (p,v)

    def update(self, p, dt=1):
        self.v, self.a, j = self.calc(p, dt)
        self.p = p
        if self.samples > 2:
            self.valid = True
        else:
            self.samples = self.samples + 1
        self.missing = 0
    def not_found(self):
        if self.valid:
            self.missing = self.missing + 1
            self.samples = self.samples - 1
        if self.samples == 0:
            self.reset()
        
motion_x = motion_tracker()
motion_y = motion_tracker()

class Candidate():
    def __init__(self):
        self.pos = (0,0)
        self.area = 0
        self.perim = 0
        self.circularity = 0
        self.score = 0
    def calc_score(self):
        dpos = 0
        if motion_x.valid and motion_y.valid:
            px,vx = motion_x.predict()
            py,vy = motion_y.predict()
            dpos = .002 * (self.pos[0] - px) ** 2 + (self.pos[1] - py) ** 2
        darea = 2 * (8.3 - self.area ** 0.5) ** 2
        dperim = (36 - self.perim) ** 2
        dcirc = 10 * (0.7 - self.circularity) ** 2
        distance = (dpos + darea + dperim + dcirc) ** 0.5
        self.score = max(0, 100 - distance)

        return self.score
    def update_motion(self):
        motion_x.update(self.pos[0], motion_x.missing+1)
        motion_y.update(self.pos[1], motion_y.missing+1)

missingFrames = 0

def get_ball_pos(state: State):
    candidates = find_candidates(state)
    select_best_candidate(state, candidates)
    display_ball_pos(state)

def find_candidates(state: State):
    hsv = cv2.cvtColor(state.frame, cv2.COLOR_BGR2HSV)

    red_low = np.array([0, 120, 25])
    red_high = np.array([7, 255, 255])
    red2_low = np.array([174, 120, 25])
    red2_high = np.array([180, 255, 255])
    curr_mask = cv2.inRange(hsv, red_low, red_high) + \
                cv2.inRange(hsv, red2_low, red2_high)
    hsv[curr_mask == 0] = 0

    img = cv2.split(hsv)[2]
    state.layers["ball"] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    candidates = []
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        candidate = Candidate()
        candidate.area = cv2.contourArea(c)
        candidate.perim = max([0.1,cv2.arcLength(c, True)])
        candidate.circularity = 4*pi*candidate.area/(candidate.perim*candidate.perim)
        if candidate.area < 50 or candidate.area > 500 or candidate.circularity < 0.4:
            continue

        x,y,w,h = cv2.boundingRect(c)
        candidate.pos = (x+w/2,y+h/2)
        candidate.calc_score()
        if candidate.score > 10:
            candidates.append(candidate)
    
    return candidates

def select_best_candidate(state: State, candidates):
    candidates.sort(key=lambda c: c.score, reverse=True)
    if len(candidates) > 0:
        #print(",".join(map(lambda c: str(c.score), candidates)))
        candidates[0].update_motion()
        bx,by = candidates[0].pos
        state.ball.set_pos(bx,by)
        return
    else:
        motion_x.not_found()
        motion_y.not_found()

    if motion_x.valid and motion_y.valid:        
        state.ball.set_pos(
            motion_x.predict(motion_x.missing)[0],
            motion_y.predict(motion_y.missing)[0],
            ObjAccuracy.Predicted)
        return

    if motion_x.p == None or motion_y.p == None:
        state.ball.set_pos(0,0,ObjAccuracy.NotFound)
        return
       
    state.ball.set_pos(motion_x.p,motion_y.p,ObjAccuracy.LastKnown)

def display_ball_pos(state: State):
    frame = np.copy(state.frame)
    state.layers["ball_pos"] = frame
    accuracy = state.ball.accuracy
    if accuracy == ObjAccuracy.NotFound:
        return
    
    color = (0,255,0)

    if accuracy == ObjAccuracy.Predicted:
        color = (0,255,255)
    if accuracy == ObjAccuracy.LastKnown:
        color = (0,0,255)

    x,y=state.ball.get()
    cv2.drawMarker(frame,(int(x),int(y)),color)
    