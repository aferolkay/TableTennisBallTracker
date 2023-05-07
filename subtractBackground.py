import cv2
import numpy as np

###### GLOBAL VARIABLES ######
website = "http://192.168.137.228:4747/video"
usb=1
webcam=0
file = "resources/tableTennisBall.mp4"

cam = cv2.VideoCapture(file)
prevDown = True
prevBottom = 0
kernel = np.ones((1,1), np.uint8  )  # for erotion

###### HELPFUL FUNCTIONS ######
def trackBall():
    # TO DO: implement ball tracking algotihms such as cam shift and mean shift etc.
    pass

def mostBallContour(contour):
    #print("Length of Detected Contours:{}".format(len(contour)))
    if len(contour)<3 :
        #return contour[0]  # TO DO: eğer top yoksa bile şu an yazdırıyo | yazdırmamasını sağla
        return None
    i = 0
    while i<3 :
        x,y,w,h = cv2.boundingRect(contour[i])
        area = cv2.contourArea(contour[i])
        aspect_ratio = float(w)/h
        rect_area = w*h
        extent = float(area)/rect_area
        if aspect_ratio>0.4 and extent >0.4 and aspect_ratio<2 :
            return contour[i]
        i+=1
    
    #print("aspect_ratio={} | extent={}".format(aspect_ratio,extent))
    #return contour[0]
    return None


    

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
    #print( " prevBottom {} --> bottom {}".format(prevBottom,bottom) )
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
    ret , thresholded = cv2.threshold( difference , 5 , 255 , cv2.THRESH_BINARY ) # here is how you change sensitivity
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
    
    #contours , hierarchy = cv2.findContours( eroded , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    contours , hierarchy = cv2.findContours( eroded , 2 , 1)
    contourSorted = sorted(contours, key=cv2.contourArea, reverse=True)

    if len(contours) != 0:            
        # TO DO: find the optimal contour
        biggestContour = mostBallContour(contourSorted)
    """
    if biggestContour != None :
        cv2.drawContours( currentFrame, contours=biggestContour, contourIdx=-1 , color=(255,255,255) ,thickness=3)        
        ret , bottomPoint = gimmeBottom(biggestContour)
        if ret == 1 :
            cv2.circle(currentFrame, bottomPoint , radius = 20 , color=(255,255,255) , thickness=-1)
    else :
        print("ağla")
    """
    try:
        if biggestContour == None :
            print("no detection")
            
    except:
        print("ov yeah detection")
        cv2.drawContours( currentFrame, contours=biggestContour, contourIdx=-1 , color=(255,255,255) ,thickness=3)        
        ret , bottomPoint = gimmeBottom(biggestContour)
        if ret == 1 :
            cv2.circle(currentFrame, bottomPoint, radius = 20 , color=(255,255,255) , thickness=-1)
    
    cv2.imshow( "CurrentFrame" , currentFrame )
    cv2.imshow( "thresholded" , thresholdedFinal)
    prevFrame = currentFrame
    currentFrame = nextFrame
    thresholdedFirst = thresholdedSecond
    if cv2.waitKey(1)  & 0xFF == 27:
        break
cam.release()
cv2.destroyAllWindows()



