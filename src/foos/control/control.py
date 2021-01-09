class Control:
    def __init__(self):
        pass

    def process(self, states):
        return {}
        
    def aim_at_ball(l):
        bx,by = l
        # 33 - 245, reduced to 235-45 = 1.9
        y = max(0,(235 - by) / 1.9)
        y = min(y,100)
        gain = 1.7    
        overlap = 4
        if y < (50+overlap):
            ry = y*gain
        else:
            ry = 100 - (100-y)*gain

        move(0,ry)
        print(f'{by:.3f} {y:.3f} {ry:.3f}')
