import cv2 as cv
import numpy as np
import imutils



videoCapture = cv.VideoCapture("tableTennisBall.mp4")

while True:
    ret, frame = videoCapture.read()
    cv.imshow("original",frame)
    if not ret: break

    resized = imutils.resize(frame, width=300)
    cv.imshow("ResolutionDown", resized)

    #converting to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("Gray", gray)

    
    #control the flow
    if cv.waitKey(6000) & 0xFF == ord('q') : break

videoCapture.release()
cv.destroyAllWindows()

