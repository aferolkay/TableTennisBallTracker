import cv2
import numpy as np
prevDown = True
prevBottom = 0
ksize = (3,3)
kernel = np.ones((3,3), np.uint8  )



def howRound(contours):
    # TO DO :
    pass

def gimmeBottom(contour):
    global prevBottom,prevDown 
    ret = 0
    point = contour[contour[:,:,0].argmin()]
    bottom = point[0,1]
    
    if prevBottom > bottom :
        down = False
    else :
        down = True
      
    if prevDown :
        if down == False:
            ret = 1
    else :
        if down == True:
            ret = 2
    print( " prewBottom {} --> bottom {}".format(prevBottom,bottom) )
    prevDown = down
    prevBottom = bottom
    return ret , tuple(point.reshape(1, -1)[0])
    



cam = cv2.VideoCapture("resources/tableTennisBall2.mp4")
ret , prevFrame = cam.read()
prevFrame = cv2.cvtColor(prevFrame , cv2.COLOR_BGR2GRAY)
prevFrame = cv2.blur( prevFrame , ksize)
# TO DO: Resolution düşürülecek

buffer = np.ones( prevFrame.shape ) * 255

while True:

    ret , currentFrame = cam.read()
    currentFrame = cv2.cvtColor(currentFrame , cv2.COLOR_BGR2GRAY)
    currentFrame = cv2.blur( currentFrame , ksize)

    temp1 = currentFrame + buffer
    temp2 = temp1 - prevFrame
    difference = temp2 - buffer
    difference = abs(difference)

    ret , thresholded = cv2.threshold( difference , 20 , 255 , cv2.THRESH_BINARY )
    thresholded = thresholded.astype(np.uint8)
    eroded = thresholded
    cv2.erode(thresholded,kernel=kernel,dst=eroded)
    contours , hierarchy = cv2.findContours( eroded , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:            
        biggestContour = max( contours , key = cv2.contourArea  )
        cv2.drawContours( currentFrame, contours=biggestContour, contourIdx=-1 , color=(255,255,255) ,thickness=3)
        
        ret , bottomPoint = gimmeBottom(biggestContour)
        if ret == 1:
            cv2.circle(currentFrame , bottomPoint , radius = 2 , color=(255,255,255) , thickness=-1)
            print("detectedddd!")
        


    

    cv2.imshow( "CurrentFrame" , currentFrame )
    cv2.imshow( "thresholded" , thresholded)

    prevFrame = currentFrame
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()