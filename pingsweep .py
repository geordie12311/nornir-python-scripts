""" This Script allows you to do a Ping Sweep of the 
Network for a specific IP subnet"""

from ipaddress import ip_network
from subprocess import check_output
from threading import Thread
from queue import Queue
#importing the libraries needed for the script


subnet = input("Enter subnet id\n>> ")
netmask = input("Enter subnetmask or CIDR\n>> ")
#user asked to input subnet and subnet mask


replies = []
#creating a blank file to capture the output

def dispatcher():
    while True:
        item = q.get()
        ping(item)
        q.task_done()
#creating a function called dipatcher to capture the input

q = Queue()

for i in range(10):
    t = Thread(target=dispatcher)
    t.daemon = True
    t.start()
#using a range loop to loop through the subnet

def ping(ip_address):
    try:
            replies.append(str(check_output('ping ' + ip_address + ' -n 1 -w 50')).split("data:")[1]
                           .split("TTL")[0].split(" ")[2][:-1])
    except:
        return
try:
    ip_range = list(ip_network(subnet+'/'+netmask))[1:-1]
    print("Scanning", ip_network(subnet+'/'+netmask))
    for ip_address in ip_range:
        q.put(str(ip_address))

    q.join()

    print("\nReachable addresses found:")
    for reply in replies:
        print(reply)

except ValueError:
    print("Error: Invalid subnet ID or subnetmask")
#creating the function to run ping the ip_address library to try pinging the ip addresses in the subnet entered by the user
#using a loop. printing the reachable IP addresses in the subnet. If incorrect subnet entered script will output an error message