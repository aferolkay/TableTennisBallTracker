from time import sleep
import cv2
import numpy as np

# TO DO: automaticaly calibrate the table with line detection algorithms in the future
keyPoints = {
            0:"Top Left Corner",
            1:"Top Right Corner",
            2:"Bottom Left Corner",
            3:"Bottom Right Corner",

            4:"Middle Left Corner",
            5:"Middle Right Corner",
            6:"Top Middle Line End Corner",
            7:"Bottom Middle Line End Corner",
            8:"Calibration Done :)"
            }
keyPts = np.zeros((8,2))
iterator = 0
lastCursor = (0,0)


def getPixelInfo(event,x,y,flags,param):
    global iterator
    global keyPts
    global lastCursor
    if iterator == 8:
        lastCursor = (x,y)
        return
    if event == cv2.EVENT_RBUTTONDOWN:
        iterator = iterator-1
        keyPts.pop()
    elif event == cv2.EVENT_LBUTTONDOWN:
        #keyPts.append(0)
        #keyPts[iterator] = (x,y)
        keyPts[iterator,0] = x
        keyPts[iterator,1] = y
        iterator = iterator+1
        
cv2.namedWindow(winname="Calibrate")
cv2.setMouseCallback("Calibrate",getPixelInfo)

def gradientDescent( pts ):
    # TO DO: BU KODU KENDINE GORE ADJUST ET    
    x = pts[:,0]
    print(x.shape)
    y = pts[:,1]
    print(y.shape)
    X, Y = np.meshgrid(x, y, copy=False)   


    # Z = X**2 + Y**2 + np.random.rand(*X.shape)*0.01
    zx = np.array([0,152,0,152 , 0,152,76,76])
    zy = np.array([0,0,274,274 , 137,137,102,172])
    Zx, Zy = np.meshgrid(x, y, copy=False)


    X = X.flatten()
    Y = Y.flatten()

    A = np.array([X*0+1, X, Y, X**2, X**2*Y, X**2*Y**2, Y**2, X*Y**2, X*Y]).T
    B = Zx.flatten()
    C = Zy.flatten()

    coeff, r, rank, s = np.linalg.lstsq(A, B)

    return coeff


cam = cv2.VideoCapture("resources/tableTennisBall.mp4")
ret, frame = cam.read()
if ret == 0:
    print("Can't get the feed")
    exit()

calibration = True
while calibration:
    
    cv2.rectangle( img=frame , pt1=(10,10) , pt2=(600,30), color = (255,255,255), thickness = 30 )  # bu fonksiyonda sıkıntı yok
    cv2.putText(img=frame , text=keyPoints[iterator],org=(10,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=1)
    cv2.imshow("Calibrate",frame)
 
    if iterator >=8 :
        
        for points in keyPts:
            cv2.circle(frame,tuple(points.astype(int)),10,(0,0,255),5)
            # TO DO: start a timer for 5 sec and set the calibration as a result
    if cv2.waitKey(1)  & 0xFF == 27:
        break

print(keyPts.shape) #(8,2)

coefficients = gradientDescent(keyPts) 

ret, frame = cam.read()
while calibration:
    
    cv2.imshow("Calibrate",frame)
    if cv2.waitKey(1)  & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()