
from serial import Serial
import time

# feedrate is being limited to 20000 mm/m ?
x_off=0
y_off=0
last_x = 0
last_y = 0
pending = False

port = Serial('/dev/ttyACM0', 115200)

def send(cmd, wait=True):
    global pending

    if pending:
        wait_for_cmd_complete()

    cmd = cmd.encode('utf-8') + b'\n'
    print(cmd)
    port.write(cmd)

    pending = True

    if wait:
        wait_for_cmd_complete()

def is_cmd_complete():
    global pending
    if pending:
        pending = read_response() != b'ok\n'
    return not pending

def wait_for_move_complete(wait = True):
    send("M400", wait)

def wait_for_cmd_complete():
    while not is_cmd_complete():
        time.sleep(.010)

def read_response():
    if port.in_waiting == 0:
        return ""

    response = port.readline()
    print(response)
    return response

def set_speed(s):
    send(f"G0 F{s}")

def home():
    send("M906")
    # disable endstops
    send("M211 S0")
    # home y
    send("M906 Y200") # set y current to 200ma
    send("G91") # relative positioning
    send("G0 F500 Y-360")
    send("G0 F500 Y20")
    send("M400") # pause until move finishes
    send("M906 X580 Y580") # set y current to 1000ma
    send("G0 F3000") # set max speed
    send("G4 P1") # wait for 1 second
    send("G90") # absolute positioning
    send("G92 X0 Y20") # set origin
    send("M122 I") # reinitialize drivers
    send("M400") # pause until move finishes
    send("G4 P1") # wait for 1 second
    init()

def move(x, y):
    global last_x
    global last_y
    x = max(0,x)
    x = min(100,x)
    y = max(0,y)
    y = min(100,y)
    if last_x != x or last_y != y:
        x_pos = x + x_off
        y_pos = y + y_off
        send("M400") # pause until move finishes
        send(f'G0 X{x_pos/2.5:.0f} Y{y_pos*3.45:.0f}')
        wait_for_move_complete(False)
        last_x = x
        last_y = y

def adjust_pos(rel_x, rel_y):
    global x_off
    global y_off
    x_off = x_off - rel_x
    y_off = y_off - rel_y
    move(last_x, last_y)

def kick():
    move(-75,50)
    move(75,50)
    move(0,50)

def init():
    # set max travel accel
    send("M204 T2000")
    send("M201 X2000 Y2000")
    send("M203 X1000 Y1000")
    send("M205 X5000 Y5000") #jerk
    send("M906 X1800 Y1000") # set y current to 1000ma
    set_speed(20000)

init()

if __name__ == "__main__":
    home()
    move(50, 50)
    move(0, 0)