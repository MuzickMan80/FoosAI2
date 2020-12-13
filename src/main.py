# Write your code here :-)
from control import *
from capture import *
from ball_detect import *
import cv2

set_speed(10000)

def aim_at_ball(l):
    bx,by = l
    # 33 - 245, reduced to 235-45 = 1.9
    y = max(0,(235 - by) / 1.9)
    y = min(y,100)
    gain = 1.7    
    overlap = 4
    if (y < (50+overlap)):
      ry = y*gain
    else:
      ry = 100 - (100-y)*gain

    move(0,ry)
    print(f'{by:.3f} {y:.3f} {ry:.3f}')

#move(0,45)

if __name__ == "__main__":
  while True:
      frame = get_frame()
      b = get_ball_pos(frame)
      if b:
          l,r=b
          display_ball_pos(frame, r)
          if is_cmd_complete():
            aim_at_ball(l)
          #print(l,r)