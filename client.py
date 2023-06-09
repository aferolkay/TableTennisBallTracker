# Echo server program
import socket
import time
import globalVariable as g
from IPaddressMap import *
mutualSocket = 0


def clientInit(connectPhone = 1 , connectInterface = 1 , connectRaspberry = 1):
    #Loopback IP address
    g.hostIP = get_local_ip()
    
    while ( (g.phoneIP==None and connectPhone) or (g.raspberryIP==None and connectRaspberry) or (g.interfaceIP==None and connectInterface) ):
        print("Scanning for other devices ...")
        clients = networkList( get_network_range() )
        print("networks scan results: {}".format(clients))
        if(g.phoneIP==None):
            g.phoneIP =  findIP( clients , MAC=g.phoneMAC)
        if(g.raspberryIP==None):
            g.raspberryIP = findIP( clients , MAC=g.raspberryMAC)
        if(g.interfaceIP==None):
            g.interfaceIP = findIP( clients , MAC=g.interfaceMAC)
        print("phoneIP: {} | raspberryIP: {} | interfaceIP: {}".format(g.phoneIP,g.raspberryIP,g.interfaceIP))
        time.sleep(1)


    print("Phone IP: {}".format(g.phoneIP))
    print("Raspberry IP: {}".format(g.raspberryIP))
    print("Interface IP: {}".format(g.interfaceIP))

    #Create a sockets
    if connectInterface:
        if g.interfaceIP != None:
            g.interfaceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            g.interfaceSocket.connect((g.interfaceIP,g.interfacePORT))
        else:
            print("interface IP could not found!")
    if connectRaspberry:
        if g.raspberryIP != None:
            g.raspberrySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            g.raspberrySocket.connect((g.raspberryIP,g.raspberryPORT))
        else :
            print("interface IP could not found!")
    
    if connectPhone:
        if g.phoneIP != None :
            g.website ="http://"+g.phoneIP+":4747/video"    #"http://192.168.55.209:4747/video"
            g.camSource = g.website
        else :
            print("phone IP could not found!, image src relayed to file")
            g.camSource = g.file

    

def sendMessage(socket,message):
    global mutualSocket
    try:
        socket.sendall(bytes(message,'utf-8'))
        return socket
    except:
        print("Could not send data, possible connection lost. Trying to connect again...")
        targetAddress = socket.getpeername()
        while ( connect(socket,targetAddress ) == 0 ):
            pass
        return mutualSocket
            
def connect( socketPrime , networkAddress ) :
    global mutualSocket
    try:
        socketPrime.close()
        socketPrime = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketPrime.connect(networkAddress)
        print("Successfully reconnected!")
        mutualSocket = socketPrime
        return 1
    except:
        print("Could not connect to the network address: {}".format(networkAddress) )
        time.sleep(1)
        return 0        


