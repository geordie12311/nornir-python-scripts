"""
Python Script to pull the hostname, IP address, Serial number,
uptime and version from devices and save the data to a CSV file
"""
import csv
import getpass
from datetime import datetime
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
#importing the libraries needed for the script

nr = InitNornir(config_file="config4.yaml") 
#The above is creating an object called nr and linking it to InitNornir and telling
#nornir which configuration file to use

user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above section will prompt the user to enter their username and password 
#and use the details input by the user to connect to the host devices.

def dev_info(task):
    r =  task.run(task=send_command, command="show version")
    task.host["facts"] = r.scrapli_response.genie_parse_output()
    serial = task.host['facts']['version']['chassis_sn']
    hoster = task.host['facts']['version']['hostname']
    up = task.host['facts']['version']['uptime']
    ver = task.host['facts']['version']['version_short']
#Creating a function called device_info that will send the command "show version" to 
#the host devices as structured data using genie parser. It is then creating objects
#for the specific structured data we want to capture from the devices which will 
#be used to populate the rows in the CSV file later in the script

    with open('device_serial_report.csv', 'w', encoding='utf8') as csvfile:
        headers = ['HOSTNAME', 'MGMT IP ADDRESS', 'SERIAL NUMBER', 'UPTIME', 'VERSION']
        header = csv.DictWriter(csvfile, fieldnames=headers, lineterminator='\n')
        header.writeheader()
        csvfile.close()
#Above section is using csv library to create the CSV file and adding the headers 
#using the fields listed in the "headers" object
        
    with open('device_serial_report.csv', 'a', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        csvdata = (hoster, task.host.hostname, serial, up, ver)
        writer.writerow(csvdata)
        csvfile.close()
#Above sectoin is opening the CSV file again and appending the data that was captured 
#in dev_info function and writing the data from each host as rows into the CSV file

result = nr.run(task=dev_info)
#Above is creating an object called results using nr.run (nornir functionality) to start
#the task "dev_info" which will send the command to the hosts, save the output as structured
#data. Then create the CSV file with the header fields and append the host information to the 
#file before finally closing the CSV file

print_result(result)
#Above is printing the data from the object result to the screen so user can view that it completed successfully