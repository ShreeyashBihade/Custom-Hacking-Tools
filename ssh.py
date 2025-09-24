import paramiko

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname="192.168.1.19", username="creator", password="1234", look_for_keys=False, allow_agent=False)

ssh = client.invoke_shell()

while True:
    command = input("$") + "\n"
    ssh.send(command)

    import time
    time.sleep(0.5)
    output = ssh.recv(4096).decode()
    print(output, end='')
