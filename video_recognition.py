# Script to read video from a camera and try to recognise some body parts
# Only for TEST purposes

import cv2 as cv
import numpy as np

# ------------- SETUP variables  ----------------------
CAMERA_ID = 1  # Index of the camera. Start with 0 and use higher if more camera devices available

# ------------- CODE ----------------------------------
# Create a VideoCapture object, the interface to communicate with the camera
cap = cv.VideoCapture(CAMERA_ID)
print("Reading Video from camera ", CAMERA_ID)
print("Frame width:", cap.get(cv.CAP_PROP_FRAME_WIDTH))
print("Frame height:", cap.get(cv.CAP_PROP_FRAME_HEIGHT))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv.imshow('Video', frame)
    # When q pressed, quit the video stream from the camera
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
