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
keyPts = []
iterator = 0

def getPixelInfo(event,x,y,flags,param):
    global iterator
    global keyPts
    if iterator == 8:
        return
    if event == cv2.EVENT_RBUTTONDOWN:
        iterator = iterator-1
        keyPts.pop()
    elif event == cv2.EVENT_LBUTTONDOWN:
        keyPts.append(0)
        keyPts[iterator] = (x,y)
        iterator = iterator+1
        
    
    
    
cv2.namedWindow(winname="Calibrate")
cv2.setMouseCallback("Calibrate",getPixelInfo)


cam = cv2.VideoCapture("resources/tableTennisBall.mp4")
ret, frame = cam.read()
if ret == 0:
    print("Can't get the feed")
    exit()

while True:
    
    cv2.rectangle( img=frame , pt1=(10,10) , pt2=(600,30), color = (255,255,255), thickness = 30 )  # bu fonksiyonda sıkıntı yok
    cv2.putText(img=frame , text=keyPoints[iterator],org=(10,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=1)
    cv2.imshow("Calibrate",frame)
 
    if iterator >=8 :
        for points in keyPts:
            cv2.circle(frame,points,10,(0,0,255),5)
    
    if cv2.waitKey(50)  & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()