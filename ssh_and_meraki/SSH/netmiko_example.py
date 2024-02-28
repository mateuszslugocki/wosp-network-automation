from netmiko import ConnectHandler

cisco_ios = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.51.11",
    username="admin",
    password="admin",
    secret="admin",
)

cisco_ios.enable()
print(cisco_ios.send_command("show platform"))
print(cisco_ios.send_command("show version"))
cisco_ios.disconnect()