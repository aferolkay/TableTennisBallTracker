import globalVariable as g
import client 
import measureTable 
import subtractBackground
from IPaddressMap import *


clientList = MACtoIP("192.168.65.1/24");
g.phoneIP = findIP( clientList, g.phoneMAC )
g.raspberryIP = findIP(clientList, g.raspberryMAC )
print(g.phoneIP)

g.website ="http://"+g.phoneIP+":4747/video"    #"http://192.168.55.209:4747/video"

g.camSource = g.website
client.clientInit(g.hostIP,8080)
#client.clientInit(g.raspberryIP,6005 )
#measureTable.initCalibration()
#measureTable.calibrate()
subtractBackground.initImageProcessing()
subtractBackground.imageProcessing(communicate=0,playrate=1, pixel_cm=0)   