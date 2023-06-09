import globalVariable as g
import client 
import measureTable 
import subtractBackground
from IPaddressMap import *

# make sure they are on the same network
client.clientInit(connectPhone = 1,connectInterface=1,connectRaspberry=1)


measureTable.initCalibration()
measureTable.calibrate(test = False)

subtractBackground.initImageProcessing()
subtractBackground.imageProcessing(communicate=1,playrate=1, pixel_cm=1)   