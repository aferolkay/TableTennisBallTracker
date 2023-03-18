import cv2 as cv
import numpy as np

def translate(img, x, y):
    transMat = np.float32( [[1,0,x],[0,1,y]] )
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]

    if rotPoint is None:
        ropPoint = ( width//2, height//2 )

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)





videoCapture = cv.VideoCapture("tableTennisBall.mp4")

while True:
    ret, frame = videoCapture.read()
    #cv.imshow("original",frame)
    if not ret: break

    #converting to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("Gray", gray)

    """
    # blurring
    blur = cv.GaussianBlur(gray, (3,3) , cv.BORDER_DEFAULT )
    cv.imshow("Blur",blur)
    
    # Edge Cascade
    canny =cv.Canny(blur, 125,175)
    cv.imshow("Edge",canny)
    
    #Dilating the image
    dilated = cv.dilate(canny, (7,7), iterations=10)
    cv.imshow("Dilated",dilated) 
 

    # Resize
    resized = cv.resize(frame,(500,250))
    cv.imshow("resized",resized)

    #Cropping
    cropped = frame[160:1700,130:1100]
    cv.imshow("Cropped",cropped)
    """
    """ 
    #shift the frame by a certain amount
    translated = translate(frame,100,100)
    cv.imshow("Translated", translated)
    """
    """
    # Rotation
    rotated = rotate(frame,45,(500,500))
    cv.imshow("Rotated", rotated)
    """
    """
    # Flipping
    flip = cv.flip(frame,1)
    cv.imshow("flipped",flip)
    """


    """
    blur = cv.GaussianBlur(gray,(3,3), cv.BORDER_DEFAULT)

    canny = cv.Canny(blur,125,175)
    cv.imshow("Canny Edges", canny)
    contours, hierarchies = cv.findContours(blur, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    """

    ret, thresh = cv.threshold(gray,125,130,cv.THRESH_BINARY)
    contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cv.imshow("Thresholding",thresh)
    #control the flow
    if cv.waitKey(6000) & 0xFF == ord('q') : break

videoCapture.release()
cv.destroyAllWindows()

