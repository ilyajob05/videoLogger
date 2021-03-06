import time
import cv2
from collections import deque
import numpy as np

def frame_diff(frames):
    img_diff0 = cv2.absdiff(frames[0], frames[1])
    img_diff1 = cv2.absdiff(frames[1], frames[2])
    return cv2.bitwise_or(img_diff0, img_diff1)

move_detector_on = True
num_queue = 3
threshold_detector = 0.001
cap = cv2.VideoCapture(0)
frames = deque(maxlen=num_queue)

morph_kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(3,3))


# get resolution
ret, frame = cap.read()
if ret != True:
    print('not frame from camera')
    exit(0)
h,w,c = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('./output_' + time.asctime() + '.avi', fourcc, 30.0, (w, h))
cv2.namedWindow('moved_mask')
cv2.namedWindow('frame')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    write_video_flag = False


    frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    if len(frames) == num_queue:
        moved_mask = frame_diff(frames)

        moved_mask = (moved_mask > 15).astype(np.uint8)
        # remove noise
        moved_mask = cv2.morphologyEx(moved_mask, cv2.MORPH_OPEN, morph_kernel)
        
        moved_val = moved_mask.sum()/(moved_mask.shape[0]*moved_mask.shape[1])
        write_video_flag = moved_val > threshold_detector
        
        print(moved_val)

        cv2.imshow('moved_mask', moved_mask*200)

    # Our operations on the frame come here -1, 0, 1, 2
    # frame = cv2.flip(frame, -1)
    frame = cv2.rectangle(frame, (0, 0), (455, 30), (0,0,0), thickness=-1)
    frame = cv2.putText(frame, time.asctime(), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), lineType=cv2.LINE_AA, thickness=2)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if write_video_flag or not move_detector_on:
        out.write(frame)
        print('write video')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()


