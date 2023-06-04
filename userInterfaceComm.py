import socket
import time
#import serial
import threading
from scapy.all import ARP, Ether, srp

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

def MACtoIP(target_ip = "192.168.65.1/24"):
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return clients
    
def findIP( clients , MAC="8c:c6:81:3b:c9:87"):
    for client in clients:
        if client['mac'] == MAC :
            return client['ip']

def connectToUserInterface(hostname):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client_socket.connect((hostname,8080))
	except :
		print("User Interface - TrainingBuddy bağlantısı kurulamadı")
		return None
	client_socket.setblocking(0)
	return client_socket

def readUserInterface(client_socket):
	try:
		data=client_socket.recv(1024)
		if data:
			data = data.decode('utf-8')
			return data
		else:
			return None
	except :
		pass

def afer_computer_ip():
	# Call the function to retrieve the local IP address
	local_ip_address = get_local_ip()
	local_ip_address = local_ip_address.split('.')
	target_ip_range = local_ip_address[0]+'.'+local_ip_address[1]+'.'+local_ip_address[2]+'.1/24'
	clients = MACtoIP(target_ip_range)
	afer_computer_ip = findIP(clients = clients)
	return afer_computer_ip

def user_Interface_Thread():
	timeout = 10;
	while 1:
		connection = None
		while connection == None:
			connection = connectToUserInterface(afer_computer_ip())
		print("Connection to userInterface has been established...")
		checkTime = time.time()
		
		while True:
			data = readUserInterface(connection)
			elapsed_time = time.time() - checkTime;
			if data != None:
				if "InterfaceON" in data:
					checkTime = time.time();
				print(data)
			
			if elapsed_time > timeout:
				print("Timeout Occured!, possible connection lost.")
				break
			
			time.sleep(1)
			print("## DO OTHER STUFF HERE")
		connection.close()

user_Interface_Thread()