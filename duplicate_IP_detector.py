"""
Script will detect duplicate IP addresses within a topology.
"""
import getpass
import logging
import os
from collections import Counter
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.password = password
#The above line is telling nornir where the config file is located

CLEAR = "clear"
os.system(CLEAR)
ip_list = []

def get_ip(task):
    """
    Parse IP addresses from all interfaces and append to ip_list
    """
    response = task.run(
        task=send_command, command="show interfaces", severity_level=logging.DEBUG
    )
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                ip_list.append(ip_addr)
        except KeyError:
            pass

def locate_ip(task):
    """
    Pull all interfaces information
    Identify the interface and Device configured with duplicate address
    """
    response = task.run(
        task=send_command, command="show interfaces", severity_level=logging.DEBUG
    )
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                if ip_addr in targets:
                    rprint(f"[yellow]{task.host} {intf} - {ip_addr}[/yellow]")
        except KeyError:
            pass

nr.run(task=get_ip)
targets = [k for k, v in Counter(ip_list).items() if v > 1]
if targets:
    rprint("[red]ALERT: DUPLICATES DETECTED![/red]")
    rprint(targets)
    rprint("\n[cyan]Locating addresses in topology...[/cyan]")
    nr.run(task=locate_ip)
else:
    rprint("[green]SCAN COMPLETED - NO DUPLICATES DETECTED[/green]")
