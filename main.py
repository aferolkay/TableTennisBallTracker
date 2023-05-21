#from globalVariable import*
#from client import*
#from measureTable import*
#from subtractBackground import *

import globalVariable
import client 
import measureTable 
import subtractBackground 




client.clientInit('169.254.4.12',6002)
#measureTable.initCalibration()
#measureTable.calibrate()
subtractBackground.initImageProcessing()
subtractBackground.imageProcessing(communicate=1,playrate=100, pixel_cm=0)