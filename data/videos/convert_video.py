import cv2

cap = cv2.VideoCapture("table_angled_processed.mp4")

aviname = f'table_angled.avi'
fourcc = cv2.VideoWriter_fourcc(*'VP80')
out = cv2.VideoWriter(aviname, fourcc, 30.0, (352,288))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame',frame)
        out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cap.release()