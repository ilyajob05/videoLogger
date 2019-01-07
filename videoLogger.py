# -*- coding: utf-8 -*-

import time
import cv2

cap = cv2.VideoCapture(0)

# get resolution
ret, frame = cap.read()
if ret != True:
    print 'not frame from camera'
    exit(0)
h,w,c = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('./output_' + time.asctime() + '.avi', fourcc, 20.0, (w, h))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here -1, 0, 1, 2
    # frame = cv2.flip(frame, -1)
    frame = cv2.rectangle(frame, (0, 0), (455, 30), (0,0,0), thickness=-1)
    frame = cv2.putText(frame, time.asctime(), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), lineType=cv2.LINE_AA, thickness=2)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()


