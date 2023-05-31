# Source: https://www.thepythoncode.com/article/building-network-scanner-using-scapy
from scapy.all import ARP, Ether, srp
import globalVariable as g

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
    
def findIP( clients , MAC="ff:ff:ff:ff:ff:ff"):
    for client in clients:
        if client['mac'] == MAC :
            return client['ip']

#print(findIP(MACtoIP("192.168.65.1/24"), g.phoneMAC ))

