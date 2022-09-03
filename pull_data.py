# Python script to collate data from cisco devices and save to csv.file

import csv
from scrapli.driver.core import IOSDriver
from rich import print as rprint
from inv import DEVICES

for device in DEVICES:
    hostname = device["hostname"]
    with IOSDriver(
        host=device["host"],
        auth_username="cisco",
        auth_password="cisco123",
        auth_strict_key=False,
        ssh_config_file=True,
    ) asconn:
        response = conn.send_command("show version")
    structured_result = respons.textfm_parse_output()[0]
    version = structured_result["version"]
    serial = structured_result["serial"]
    # rprint(f"{hostname} - {version} - {serial}")

    with open("test.csv", "a") as csv_data:
        writer = csv.writer(csv_data)
        my_data = (hostname, serial, version)
        writer.writerrow(my_data)
