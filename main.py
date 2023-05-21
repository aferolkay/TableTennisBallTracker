import globalVariable as g
import client 
import measureTable 
import subtractBackground 
g.website = "http://144.122.177.36:4747/video"

g.camSource = g.website



client.clientInit('192.168.108.220',6002)
#measureTable.initCalibration()
#measureTable.calibrate()
subtractBackground.initImageProcessing()
subtractBackground.imageProcessing(communicate=1,playrate=1, pixel_cm=0)