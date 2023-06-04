# Source: https://www.thepythoncode.com/article/building-network-scanner-using-scapy
from scapy.all import ARP, Ether, srp
import socket
import globalVariable as g

def get_network_range():
	# Call the function to retrieve the local IP address
	local_ip_address = get_local_ip()
	local_ip_address = local_ip_address.split('.')
	target_ip_range = local_ip_address[0]+'.'+local_ip_address[1]+'.'+local_ip_address[2]+'.1/24'
	return target_ip_range

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


def networkList(target_ip = "192.168.65.1/24"):

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
    
def findIP( clients , MAC="ff:ff:ff:ff:ff:ff"):
    for client in clients:
        if client['mac'] == MAC :
            return client['ip']

