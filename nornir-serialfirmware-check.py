"""
Python script to interogate the hosts for serial number
and firmware version. Also carries out a validity check
of the firmware version to check it is compliant
"""
### Importing libraries
import time #importing time for pause in output
import getpass #importing getpass to handle the password for the hosts
from nornir import InitNornir #using nornir so importing InitNornir to initiate the script
from nornir_scrapli.tasks import send_command # importing scrapli send_command function
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen
from rich import print as rprint #importing print from rich to provide a more colourful output

nr = InitNornir(config_file="config3.yaml") #Initiating Nornir using config.yaml as configuration file

### User credential section:
userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

userName = input(userNamePrompt) #using user inputted username to pass username to host(s)
password = getpass.getpass(passPrompt) #using getpass to pass the password to host(s)
nr.inventory.defaults.username = userName #using userName input for username to login
nr.inventory.defaults.password = password #using password input for password to authenticate

host_table_header = ["Hostname", "Serial Number", "Version"]
check_table_header = ["Pass", "Fail"]

### Functional Script section:
def pull_data(task):
    ver_result = task.run(task=send_command, command="show version") #using scrapli to send the command
    task.host["facts"] = ver_result.scrapli_response.genie_parse_output() #using genie to parse out the structured data as "facts" object
    version = task.host["facts"]["version"]["version"] #using the data in the facts object to pull out the version
    uptime = task.host["facts"]["version"]["uptime"] #using the data in the facts object to pull out the uptime
    serial_num = task.host["facts"]["version"]["chassis_sn"] #using the data in the facts object to pull out serial number
 
    rprint(f"{task.host} serial number is: {serial_num}. Firmware version is: {version}.") #printing the outputs
    time.sleep(1) #sleeping for 1sec

    if version == "15.7(3)M3": #version check
        time.sleep(1) #sleeping for 1sec
        rprint(f"{task.host}: CHECK VERSION is: {version}. [green]CHECK PASSED![/green]") #validating the version is 15.7(3)M3
    else:
        time.sleep(1) #sleeping for 1sec
        rprint(f"{task.host}: CHECK VERSION is: {version}. [red]CHECK FAILED![/red]") #if version does not pass validation printing check failed
    
    with open("host_serial_version.csv", "w") as file:
        writer = csv.writer()
        writer.writerow(host_table_header)
        writer.writerow(f"{task.host}, {serial_num}, {version}")
result = nr.run(task=pull_data) #printing the output from the pull_data function to the screen