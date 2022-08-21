"""
Script to create a Ping report using Rich
"""
import os
import time
from datetime import date
from subprocess import Popen, DEVNULL
from rich.console import Console
from rich.table import Table
import itertools

clear = "clear"
os.system(clear)
localtime = time.asctime(time.localtime(time.time()))
active_list = []
inactive_list = []
p = {}
with open('reader.txt', 'r') as f:
    filelines = f.readlines()
for n in filelines:
    ip = n
    p[ip] = Popen(['ping', '-c', '4', '-i', '0.2', ip], stdout=DEVNULL)

while p:
    for ip, proc in p.items():
        if proc.poll() is not None:
            del p[ip]
            if proc.returncode == 0:
                active_list.append(ip)
            elif proc.returncode == 1:
                inactive_list.append(ip)
            else:
                print(f"{ip} ERROR")
            break

table = Table(title="PING REPORT \n" + localtime)
table.add_column("Active Hosts", justify="center", style="green")
table.add_column("Inactive Hosts", justify="center",style="red")
for (a,i) in itertools.zip_longest(active_list,inactive_list):
    table.add_row(a,i)
console = Console()
console.print(table)