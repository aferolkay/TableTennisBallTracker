# Echo server program
import socket
import time

def get_local_ip():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't matter which)
        sock.connect(("8.8.8.8", 80))
        # Get the local IP address
        local_ip = sock.getsockname()[0]
        # Close the socket
        sock.close()
        return local_ip
    except socket.error:
        return None
    
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


