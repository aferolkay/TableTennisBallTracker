# Echo server program
import socket
import time
import serial
import threading

imageFlag=0
vibrationFlag=0


def image_reset():
    global imageFlag
    imageFlag=0
    
def vibration_reset():
    global vibrationFlag
    vibrationFlag=0
    
def checkSync():
    global imageFlag
    global vibrationFlag
    if imageFlag and vibrationFlag :
        print("SYNCHRONIZATION!!!")
    else:
        if imageFlag:
            print("ONLY IMAGE!!!")
        else:
            if vibrationFlag:
                print("ONLY VIBRATION!!!")
        
    
vibrationTimer = threading.Timer(0.1, vibration_reset)
imageTimer = threading.Timer(0.1, image_reset)

    
# Create serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()
	

#Loopback IP address
HOST = '192.168.243.220'
PORT = 6002
#Create a sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
print ("Socket is bound to IP:",HOST," PORT:",PORT)
server_socket.listen(1)
print("Listening for connections")
conn, clientAddress = server_socket.accept()
print ('Proxy is connected to the client ', clientAddress)


while 1:
	if ser.in_waiting > 0:
    
        vibrationFlag = 1
        vibrationTimer.start()
        
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
        
			
    try:
        dataReceived = conn.recv(1024)
    except OSError:
        print (clientAddress, 'disconnected')
        server_socket.listen(1)
        conn, clientAddress = server_socket.accept()
        print ('Connected by', clientAddress)
        time.sleep(0.5)

    else:
        imageFlag = 1
        imageTimer.start()
        
        dataReceived = dataReceived.decode('utf-8')
        print(dataReceived)
      
