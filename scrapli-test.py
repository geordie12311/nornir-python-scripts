from scrapli.driver.core import IOSXEDriver

my_device = {
    "host": "NN-SW-03",
    "auth_username": "cisco",
    "auth_password": "cisco123",
    "auth_strict_key": False,
}

conn = IOSXEDriver(**my_device)
conn.open()
response = conn.send_command("show ip int brief")
print(response.result)