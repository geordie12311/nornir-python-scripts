
import getpass
from ipaddress import ip_network, ip_address
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen

nr = InitNornir(config_file="config3.yaml") #Initiating Nornir using config.yaml as configuration file


### User credential section:
userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

### User credential section:
userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

userName = input(userNamePrompt) #using user inputted username to pass username to host(s)
password = getpass.getpass(passPrompt) #using getpass to pass the password to host(s)
nr.inventory.defaults.username = userName #using userName input for username to login
nr.inventory.defaults.password = password #using password input for password to authenticate

target = input("Enter the target IP address: ")
ipaddr = ip_address(target)

def get_routes(task):
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        print(f" {task.host} is connected to {target} via interface {exit_intf}")
                except KeyError:
                    pass
        
nr.run(task=get_routes)