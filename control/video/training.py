# This module generates videos for training a CNN to detect the
# rod rotation and translation
from control import move, set_speed, is_cmd_complete
from capture import get_frame
import cv2
from random import randint
import csv

x = 0
y = 0
chunk = 1

with open('settings.tsv', 'wt') as settings_file:
    settings_writer = csv.writer(settings_file, delimiter='\t')

    while chunk < 40:
        new_x = -37.5 + 12.5 * randint(0,6)
        new_y = 0 + 25 * randint(0,4)
        if new_x == x and new_y == y:
            continue
        frame_cnt = 0
        aviname = f'chunk{chunk}.avi'
        fourcc = cv2.VideoWriter_fourcc(*'HFYU')
        out = cv2.VideoWriter(aviname, fourcc, 30.0, (352,288))

        move(new_x, new_y)
        while not is_cmd_complete():
            frame = get_frame()
            out.write(frame)
            cv2.imshow('frame', frame)
            frame_cnt = frame_cnt + 1

        out.release()

        chunkname = f'chunk{chunk}.tsv'
        with open(chunkname, 'wt') as chunk_file:
            chunk_writer = csv.writer(chunk_file, delimiter='\t')
            skip_frames = 3
            move_frames = frame_cnt - skip_frames
            delta_x = (new_x - x)/move_frames
            delta_y = (new_y - y)/move_frames
            for frame_id in range(1, frame_cnt):
                if frame_id >= skip_frames:
                    x = x + delta_x
                    y = y + delta_y
                chunk_writer.writerow([x/100, y/100])
        settings_writer.writerow([aviname, chunkname])
        x = new_x
        y = new_y
        chunk = chunk + 1

move(0,0)