import cv2
import numpy as np

###### GLOBAL VARIABLES ######
website = "http://192.168.118.209:4747/video"
websiteBasak = "http://192.168.118.233:4747/video"
usb=1
webcam=0
file = "resources/tableTennisBall.mp4"

cam = cv2.VideoCapture(1)
prevDown = True
prevBottom = 0
kernel = np.ones((3,3), np.uint8  )  

###### HELPFUL FUNCTIONS ######
def trackBall():
    # TO DO: implement ball tracking algotihms such as cam shift and mean shift etc.
    pass
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
        if (down == False)  & (bottom > 65):  
            ret = 1
    else :
        if down == True:
            ret = 2
    print( " prewBottom {} --> bottom {}".format(prevBottom,bottom) )
    prevDown = down
    prevBottom = bottom
    return ret , tuple(point.reshape(1, -1)[0])        

def getFrame(src = cam, kernelsize = (3,3) , downScale = 100):
    ret , frame = src.read()
    if ret == False:
        print("Can't get the video feed.")
        exit()
    frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    width = int(frame.shape[1] * downScale / 100)
    height = int(frame.shape[0] * downScale / 100)
    dim = (width , height)
    frame = cv2.resize(src=frame , dsize=dim  , interpolation = cv2.INTER_AREA )
    frame = cv2.blur( frame , kernelsize)
    return frame

def thresholdedDifference(frame1 , frame2 , buffer):
    temp1 = frame2 + buffer
    temp2 = temp1 - frame1
    difference = temp2 - buffer
    difference = abs(difference)
    ret , thresholded = cv2.threshold( difference , 20 , 255 , cv2.THRESH_BINARY )
    thresholded = thresholded.astype(np.uint8)
    return thresholded


###### MAIN PART ######
prevFrame = getFrame(src = cam)
currentFrame = getFrame()
buffer = np.ones( prevFrame.shape ) * 255
thresholdedFirst = thresholdedDifference(prevFrame,currentFrame,buffer)

while True:

    nextFrame = getFrame() 
    thresholdedSecond = thresholdedDifference(currentFrame,nextFrame,buffer)
    thresholdedFinal = thresholdedFirst & thresholdedSecond
    
    eroded = thresholdedFinal
    cv2.erode(thresholdedFinal,kernel=kernel,dst=eroded)
    
    contours , hierarchy = cv2.findContours( eroded , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:            
        biggestContour = max( contours , key = cv2.contourArea  )
        cv2.drawContours( currentFrame, contours=biggestContour, contourIdx=-1 , color=(0,255,255) ,thickness=3)
        
        ret , bottomPoint = gimmeBottom(biggestContour)
        if ret == 1 :
            cv2.circle(currentFrame , bottomPoint , radius = 20 , color=(255,255,255) , thickness=-1)
            print("detectedddd!")    

    cv2.imshow( "CurrentFrame" , currentFrame )
    cv2.imshow( "thresholded" , thresholdedFinal)

    prevFrame = currentFrame
    currentFrame = nextFrame
    thresholdedFirst = thresholdedSecond
    if cv2.waitKey(1)  & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()