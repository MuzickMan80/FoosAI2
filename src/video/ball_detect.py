import cv2
import numpy as np
from math import pi

def get_ball_pos(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_low = np.array([0, 100, 50])
    red_high = np.array([5, 255, 255])
    red2_low = np.array([174, 100, 50])
    red2_high = np.array([180, 255, 255])
    curr_mask = cv2.inRange(hsv, red_low, red_high) + cv2.inRange(hsv, red2_low, red2_high)
    hsv[curr_mask == 0] = 0

    img = cv2.split(hsv)[2]

    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        perim = max([0.1,cv2.arcLength(c, True)])
        circularity = 4*pi*area/(perim*perim)
        if area < 50 or area > 500 or circularity < 0.4:
            continue

        x,y,w,h = rect
        return ((x+w/2,y+h/2),rect)

def display_ball_pos(frame,r):
    x,y,w,h = r
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("ball",frame)
    cv2.waitKey(1)