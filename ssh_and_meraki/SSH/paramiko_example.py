import paramiko
import time

ip = '192.168.51.11'
port = 22
username = 'admin'
password = 'admin'

client = paramiko.SSHClient()

client.load_system_host_keys()
client.connect(ip, port, username, password)

commands = client.invoke_shell()
commands.send("en\n")
commands.send(f"{password}\n")
commands.send("terminal length 0\n")
commands.recv(65535)
commands.send("show platform\n")
time.sleep(1)
output = commands.recv(65535).decode("utf-8")
print(output)
commands.send("show version\n")
time.sleep(1)
output = commands.recv(65535).decode("utf-8")
print(output)
