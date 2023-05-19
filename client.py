# Echo server program
import socket
import time

def clientInit(hostIP,portNO):
    global HOST
    global PORT
    global client_socket
    
    #Loopback IP address
    HOST = hostIP
    PORT = portNO
    #Create a sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

def sendMessage(message):
    client_socket.sendall(bytes(message,'utf-8'))


