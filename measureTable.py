from time import sleep
import cv2
import numpy as np
import globalVariable as g

def initCalibration():
    # TO DO: automaticaly calibrate the table with line detection algorithms in the future
    g.keyPoints = {
                0:"Top Left Corner",
                1:"Top Right Corner",
                2:"Bottom Left Corner",
                3:"Bottom Right Corner",

                4:"Middle Left Corner",
                5:"Middle Right Corner",
                6:"Top Middle Line End Corner",
                7:"Bottom Middle Line End Corner",
                8:"Top Middle Line ",
                9:"Bottom Middle Line ",
                10:"Calibration Done :)"
                }
    g.keyPts = np.zeros((10,2))
    g.iterator = 0
    g.lastCursor = (0,0)

def getPixelInfo(event,x,y,flags,param):
    if g.iterator == 10:
        g.lastCursor = (x,y)
        return
    if event == cv2.EVENT_RBUTTONDOWN:
        g.iterator = g.iterator-1
        g.keyPts.pop()
    elif event == cv2.EVENT_LBUTTONDOWN:
        g.keyPts[g.iterator,0] = x
        g.keyPts[g.iterator,1] = y
        g.iterator = g.iterator+1
        
def gradientDescent( pts ):
    X = pts[:,0] / 10    # Px array
    print(X)
    Y = pts[:,1] / 10   # Py array
    
    zx = np.array([0,152,0,152 , 0 , 152,76 , 76, 76,76])
    zy = np.array([0,0,274,274 , 137,137,102,172,0,274])
    
    A = np.array( [[X[0]*0+1, X[0], Y[0], X[0]**2, X[0]**2*Y[0], X[0]**2*Y[0]**2, Y[0]**2, X[0]*Y[0]**2, X[0]*Y[0]], 
                  [X[1]*0+1, X[1], Y[1], X[1]**2, X[1]**2*Y[1], X[1]**2*Y[1]**2, Y[1]**2, X[1]*Y[1]**2, X[1]*Y[1]] , 
                  [X[2]*0+1, X[2], Y[2], X[2]**2, X[2]**2*Y[2], X[2]**2*Y[2]**2, Y[2]**2, X[2]*Y[2]**2, X[2]*Y[2]] , 
                  [X[3]*0+1, X[3], Y[3], X[3]**2, X[3]**2*Y[3], X[3]**2*Y[3]**2, Y[3]**2, X[3]*Y[3]**2, X[3]*Y[3]] , 
                  [X[4]*0+1, X[4], Y[4], X[4]**2, X[4]**2*Y[4], X[4]**2*Y[4]**2, Y[4]**2, X[4]*Y[4]**2, X[4]*Y[4]] , 
                  [X[5]*0+1, X[5], Y[5], X[5]**2, X[5]**2*Y[5], X[5]**2*Y[5]**2, Y[5]**2, X[5]*Y[5]**2, X[5]*Y[5]] , 
                  [X[6]*0+1, X[6], Y[6], X[6]**2, X[6]**2*Y[6], X[6]**2*Y[6]**2, Y[6]**2, X[6]*Y[6]**2, X[6]*Y[6]] , 
                  [X[7]*0+1, X[7], Y[7], X[7]**2, X[7]**2*Y[7], X[7]**2*Y[7]**2, Y[7]**2, X[7]*Y[7]**2, X[7]*Y[7]] ,
                  [X[8]*0+1, X[8], Y[8], X[8]**2, X[8]**2*Y[8], X[8]**2*Y[8]**2, Y[8]**2, X[8]*Y[8]**2, X[8]*Y[8]] ,
                  [X[9]*0+1, X[9], Y[9], X[9]**2, X[9]**2*Y[9], X[9]**2*Y[9]**2, Y[9]**2, X[9]*Y[9]**2, X[9]*Y[9]]])

    coeffx, r, rank, s = np.linalg.lstsq(A, zx)
    coeffy, r, rank, s = np.linalg.lstsq(A, zy)

    return coeffx,coeffy

def calibrate(test = 1):

    cv2.namedWindow(winname="Calibrate")
    cv2.setMouseCallback("Calibrate",getPixelInfo)

    cam = cv2.VideoCapture(g.camSource)
    ret, frame = cam.read()
    if ret == 0:
        print("Can't get the feed")
        exit()

    # CALIBRATION WITH USER INPUT
    calibration = True
    while True:
        temp = frame.copy()
        #cv2.rectangle( img=frame , pt1=(10,10) , pt2=(600,30), color = (255,255,255), thickness = 30 )  # bu fonksiyonda sıkıntı yok
        cv2.putText(img=temp , text=g.keyPoints[g.iterator],org=(10,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 255),thickness=1)
        cv2.imshow("Calibrate",temp)
        if g.iterator >=10 : 
            break
            #for points in keyPts:
                #cv2.circle(frame,tuple(points.astype(int)),10,(0,0,255),5)
                # TO DO: start a timer for 5 sec and set the calibration as a result
                #pass
        if cv2.waitKey(1)  & 0xFF == 27:
            break
    g.coefficientX,g.coefficientY = gradientDescent(g.keyPts) 
    
    
    if test :
        # TEST WHETHER CALCULATIONS ARE CORRECT
        #cam = cv2.VideoCapture(g.camSource)
        ret, frame = cam.read()
        while True:
            X = g.lastCursor[0]/10
            Y = g.lastCursor[1]/10
            cursorMatrix = np.array([X*0+1, X, Y, X**2, X**2*Y, X**2*Y**2, Y**2, X*Y**2, X*Y])
            xLocation = np.matmul( g.coefficientX , cursorMatrix )
            yLocation = np.matmul( g.coefficientY , cursorMatrix )
            cv2.rectangle( img=frame , pt1=(10,10) , pt2=(600,30), color = (255,255,255), thickness = 30 )  
            cv2.putText(img=frame , text= str(int(xLocation))+","+str(int(yLocation))      ,org=(10,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=1)
            cv2.imshow("Calibrate",frame)
            if cv2.waitKey(10)  & 0xFF == 27:
                break
    cam.release()
    cv2.destroyAllWindows()
    print("Calibration done! Switching to image processing")
    sleep(1)




























"""
# TEST WHETHER CALCULATIONS ARE CORRECT
ret, frame = cam.read()
while False:
    X = lastCursor[0]
    Y = lastCursor[1]
    cursorMatrix = np.array([X*0+1, X, Y, X**2, X**2*Y, X**2*Y**2, Y**2, X*Y**2, X*Y]).T
    xLocation = np.matmul( coefficientX , cursorMatrix )
    yLocation = np.matmul( coefficientY , cursorMatrix )
    cv2.rectangle( img=frame , pt1=(10,10) , pt2=(600,30), color = (255,255,255), thickness = 30 )  
    cv2.putText(img=frame , text= str(int(xLocation))+","+str(int(yLocation)) ,org=(10,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=1)

    cv2.imshow("Calibrate",frame)
    if cv2.waitKey(10)  & 0xFF == 27:
        break
"""
