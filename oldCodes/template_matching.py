import numpy as np
import cv2                                                    



template = cv2.imread("BallTracking/resources/ballScreenshot3.png",0)

methods = [ cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED ]

h,w = template.shape

for method in methods:
    capture = cv2.VideoCapture('BallTracking/resources/tableTennisBall.mp4')
    last_frame_num = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("flag")
    count = 0
    while True:
        (ret, frame) = capture.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        img2 = img.copy()
 
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc

        bottom_right = (location[0] + w, location[1] + h)
        cv2.rectangle(img2, location, bottom_right, 255, 3)
        cv2.imshow("Match",img2)
        cv2.waitKey(1)
        count+=1
        if (last_frame_num - 3 < count) :
            capture.release()
            cv2.destroyAllWindows()
            break

         