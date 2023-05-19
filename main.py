#from globalVariable import*
#from client import*
#from measureTable import*
#from subtractBackground import *

import globalVariable
import client 
import measureTable 
import subtractBackground 




#client.clientInit('192.168.243.220',6002)

measureTable.initCalibration()
measureTable.calibrate()
subtractBackground.initImageProcessing()
subtractBackground.imageProcessing()