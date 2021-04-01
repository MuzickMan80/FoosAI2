import cv2
import numpy as np
from foos.state import StateHistory, ObjAccuracy

lastFrame = None

def mouse(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE and not lastFrame is None:
        val = lastFrame[y,x]
        hsv = cv2.cvtColor(np.uint8([[val]]), cv2.COLOR_BGR2HSV)
        print(f'{x},{y} H{hsv[0,0,0]} S{hsv[0,0,1]} B{hsv[0,0,2]}')

def nothing(*args):
    pass

class Display():
    def __init__(self):
        cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("frame",702,576)
        cv2.setMouseCallback("frame", mouse)
        cv2.createTrackbar("layer","frame",0,0,nothing)
        pass

    def show(self, states: StateHistory, update):
        state = states.state0

        layers = list(state.layers.values())
        cv2.setTrackbarMax("layer","frame",len(layers))
        layer = cv2.getTrackbarPos("layer","frame")
        frame = state.frame
        if layer > 0:
            frame = layers[layer-1]

        global lastFrame
        lastFrame = np.copy(frame)

        cv2.putText(lastFrame, str(state.frame_id), (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0))
        
        cv2.imshow("frame",lastFrame)
        cv2.waitKey(1)

    