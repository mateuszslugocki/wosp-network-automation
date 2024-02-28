import pexpect

username = "admin"
password = "admin"
ip = "192.168.51.11"
hostname = "R1"

child = pexpect.spawn(f"ssh -o KexAlgorithms=diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa {username}@{ip}")
child.expect("Password:")
child.sendline(password)
child.expect(f"{hostname}>")
child.sendline("en")
child.expect("Password:")
child.sendline(password)
child.expect(f"{hostname}#")
child.sendline("terminal length 0")
child.expect(f"{hostname}#")
child.sendline("show platform")
child.expect(f"{hostname}#")
output = child.before.decode()
print(output)
child.sendline("show version")
child.expect(f"{hostname}#")
output = child.before.decode()
print(output)
