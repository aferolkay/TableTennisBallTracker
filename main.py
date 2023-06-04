import globalVariable as g
import client 
import measureTable 
import subtractBackground
from IPaddressMap import *

# make sure they are on the same network
client.clientInit(connectPhone = 0,connectInterface=1,connectRaspberry=0)


#measureTable.initCalibration()
#measureTable.calibrate()

subtractBackground.initImageProcessing()
subtractBackground.imageProcessing(communicate=1,playrate=1, pixel_cm=0)   