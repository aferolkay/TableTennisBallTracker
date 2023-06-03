import subprocess
import re
import globalVariable as g
def find_all_instances(string, substring):
    matches = re.finditer(substring, string)
    indices = [match.start() for match in matches]
    return indices

def findIPfromMAC(MACaddress):
    output = subprocess.check_output(("arp", "-a"))
    output = output.decode(encoding = 'UTF-8')
    output = output.split("Interface: ")

    for interface in output:
        if interface.find(MACaddress)  != -1:
            MACindex =interface.find(MACaddress)
            IPindexes = find_all_instances (interface,interface[0:3])
            filtered_list = [value for value in IPindexes if value < MACindex]
            IPindex = filtered_list[-1]
            IP =  interface[IPindex : MACindex].replace(" ","")
            print(IP)
            return IP
    
findIPfromMAC(g.phoneMAC)

