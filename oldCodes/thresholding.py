import cv2 as cv
import numpy as np

#videoCapture = cv.VideoCapture("tableTennisBall.mp4")

videoCapture = cv.VideoCapture(0)

"""
img = cv.imread("renkliToplar.png")
#converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
output = gray.copy()
cv.imshow("Gray", gray)
gray = cv.medianBlur(gray, 5)
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=50, maxRadius= 100   )
detected_circles = np.uint16(np.around(circles))
for (x,y,r) in detected_circles[0,:]:
    cv.circle(output, (x,y), r, (2,255,0), 3)
    cv.circle(output, (x,y), 2, (255,255,0), 3)

cv.imshow("output",output)
cv.waitKey(0)
cv.destroyAllWindows()
"""


while True:
    ret, frame = videoCapture.read()
    #cv.imshow("original",frame)
    if not ret: break

    #converting to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    output = gray.copy()
    cv.imshow("Gray", gray)
    gray = cv.medianBlur(gray, 5)

    


    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.5, 20, param1=50, param2=30, minRadius=30, maxRadius= 40   )
    detected_circles = np.uint16(np.around(circles))
    
    

    for (x,y,r) in detected_circles[0,:]:
        cv.circle(output, (x,y), r, (2,255,0), 3)
        cv.circle(output, (x,y), 2, (255,255,0), 3)
                     
    cv.imshow("output",output)

    #control the flow
    if cv.waitKey(16) & 0xFF == ord('q') : break

videoCapture.release()
cv.destroyAllWindows()

