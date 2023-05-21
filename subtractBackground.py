import cv2
import numpy as np
from collections import deque
import globalVariable as g
import client





def initImageProcessing():
    ###### GLOBAL VARIABLES ######
    global website
    global usb
    global webcam
    global file
    global bufferSize
    global cam
    global prevDown
    global prevBottom
    global kernel
    global pts

    

    cam = cv2.VideoCapture(g.camSource)
    prevDown = True
    prevBottom = 0
    kernel = np.ones((1,1), np.uint8  )  # for erotion
    pts = deque(maxlen=g.bufferSize)  # to draw connections between balls


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

def getFrame(src, kernelsize = (3,3) , downScale = 100,loop = 0):
    ret , frame = src.read()
    if ret == False:
        if loop :
            src.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame =  getFrame(src = src)
            return frame
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
    ret , thresholded = cv2.threshold( difference , 20 , 255 , cv2.THRESH_BINARY ) # here is how you change sensitivity
    thresholded = thresholded.astype(np.uint8)
    return thresholded

def imageProcessing(communicate = 0, playrate=1 , pixel_cm = 1):
    global website
    global usb
    global webcam
    global file
    global bufferSize
    global cam
    global prevDown
    global prevBottom
    global kernel
    global pts
    

    ###### MAIN PART ######
    biggestContour = 0
    prevFrame = getFrame(src = cam)
    currentFrame = getFrame(src = cam)
    buffer = np.ones( prevFrame.shape ) * 255
    thresholdedFirst = thresholdedDifference(prevFrame,currentFrame,buffer)

    while True:
        nextFrame = getFrame(src = cam , loop = 1) 
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
        
        try:
            if biggestContour == None :
                #print("no detection")
                pts.appendleft(None)
            
        except:
            #print("ov yeah detection")
            
            # to calculate the center
            M = cv2.moments(biggestContour)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            pts.appendleft(center)
            # calclulate sender ended

            cv2.drawContours( currentFrame, contours=biggestContour, contourIdx=-1 , color=(255,255,255) ,thickness=3)        
            ret , bottomPoint = gimmeBottom(biggestContour)
            if ret == 1 :
                cv2.circle(currentFrame, bottomPoint, radius = 20 , color=(255,255,255) , thickness=-1)
                x=bottomPoint[0] // 5
                y=bottomPoint[1] // 5
                if pixel_cm :
                    cursorMatrix = np.array([x*0+1, x, y, x**2, x**2*y, x**2*y**2, y**2, x*y**2, x*y],dtype=np.int64).T
                    xLocation = int(np.matmul( g.coefficientX , cursorMatrix ))
                    yLocation = int(np.matmul( g.coefficientY , cursorMatrix ))
                else:
                    xLocation = x
                    yLocation = y
                if yLocation > 165 :
                    print("Başarılı:{},{}".format(xLocation,yLocation))
                    if communicate:
                        client.sendMessage("Başarılı:{},{}".format(xLocation,yLocation))
                else :
                    print("Başarısız:{},{}".format(xLocation,yLocation))
                    if communicate:
                        client.sendMessage("Başarısız:{},{}".format(xLocation,yLocation))
        
                    
        
        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(g.bufferSize / float(i + 1)) * 2.5 ) #2.5
            cv2.line(currentFrame, pts[i - 1], pts[i], (255, 255, 255), thickness)
        
        
        
        
        
        cv2.imshow( "CurrentFrame" , currentFrame )
        cv2.imshow( "thresholded" , thresholdedFinal)
        prevFrame = currentFrame
        currentFrame = nextFrame
        thresholdedFirst = thresholdedSecond
        if cv2.waitKey(playrate)  & 0xFF == 27:
            break
    cam.release()
    cv2.destroyAllWindows()



