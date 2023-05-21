import socket
import time
import serial
import threading

imageFlag=0
vibrationFlag=0

def image_reset():
	global imageFlag
	imageFlag=0	
	print("image timer up and image flag cleared")
def vibration_reset():
	global vibrationFlag
	vibrationFlag=0	
	print("vibration timer up and vibration flag cleared")
def vibrationTimer():
	vibrationTimer = threading.Timer(1, vibration_reset)
	vibrationTimer.start()
def imageTimer():
	imageTimer = threading.Timer(1, image_reset)
	imageTimer.start()	
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




# Create serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()



# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('169.254.4.12', 6002)

# Bind the socket to the server address and port
server_socket.bind(server_address)

while True:
	# Listen for incoming connections (maximum of 1 connection)
	server_socket.listen(1)
	print("Waiting for a connection...")

	# Accept a client connection
	client_socket, client_address = server_socket.accept()
	print("Client connected:", client_address)

	# Set the socket to non-blocking mode
	client_socket.setblocking(0)

	while True:
		try:
			# Receive data from the client
			data = client_socket.recv(1024)

			# Check if data was received
			if data:
				# Process the received data
				data = data.decode('utf-8')
				print("Received data:", data)
				imageFlag = 1
				imageTimer()
				checkSync()
				
			else:
				# No data received, client has disconnected
				print("Client disconnected")
				break
		except socket.error as e:
			# No data available to be read
			error_code = e.args[0]
			if error_code == socket.errno.EWOULDBLOCK:
				# Handle the absence of data gracefully
				# ...
				pass

		# Continue with other tasks
		# ...
		
		if ser.in_waiting > 0:
	
			vibrationFlag = 1
			vibrationTimer()
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			checkSync()
		

	# Close the client socket
	client_socket.close()

# Close the server socket
server_socket.close()
