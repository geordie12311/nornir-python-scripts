from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.tasks.files import transfer_file
from nornir.plugins.functions.text import print_result
from getpass import getpass

# Ask for the new firmware file and the login credentials
firmware_file = input('Enter the firmware file name (including path): ')
username = input('Enter the username: ')
password = getpass('Enter the password: ')

# Initialize Nornir with the inventory file
nr = InitNornir(config_file='config.yaml')

# Define the function to upgrade a switch
def upgrade_switch(switch, firmware_file, username, password):
    # Transfer the firmware file to the switch
    result = switch.run(
        task=transfer_file,
        src=firmware_file,
        dest=f'/bootflash/{firmware_file.split("/")[-1]}'
    )
    print_result(result)

    # Configure the switch to boot from the new firmware
    commands = [
        'config t',
        f'boot system switch all flash:{firmware_file.split("/")[-1]}',
        'end'
    ]
    result = switch.run(
        task=netmiko_send_config,
        config_commands=commands
    )
    print_result(result)

    # Save the running configuration to the startup configuration
    result = switch.run(
        task=netmiko_send_command,
        command_string='write memory'
    )
    print_result(result)

    # Reboot the switch to boot from the new firmware
    result = switch.run(
        task=netmiko_send_command,
        command_string='reload',
        delay_factor=2
    )
    print_result(result)

# Call the function to upgrade the switches in the inventory
result = nr.run(
    task=upgrade_switch,
    firmware_file=firmware_file,
    username=username,
    password=password
)
print_result(result)