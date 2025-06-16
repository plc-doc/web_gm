import subprocess

# result = subprocess.run(['ip a', '-l'], capture_output=True, text=True)
# print(result.stdout)  # Вывод стандартного потока вывода

# result = subprocess.check_output("ifconfig", shell=True, text=True)
#
# print(result)

# result = subprocess.run(["ifconfig"], capture_output=True, text= True, check= True)
# print(result.stdout)
current_eth0_ip = "ifconfig eth0| grep 'inet' | cut -d: -f2 | awk '{print $2}'"

# class IP:
#     def __init__(self, name):
#         self.name = name
#
#     def get_ip4(self):
#         result = subprocess.run(["ifconfig eth0| grep 'inet' | cut -d: -f2 | awk '{print $2}'"], shell=True,
#                                 capture_output=True, text=True, check=True)
#         return result.stdout

# result = subprocess.run(["cat", "/etc/network/interfaces"], capture_output=True, text=True)
# print(result.stdout)

new_config = '''\
'''

# process = subprocess.run(['sudo', 'tee', "/etc/network/interfaces"], input= new_config, text=True)

#read configuration file
result = subprocess.run(["cat", "/etc/network/interfaces"], capture_output=True, text=True)
print(result.stdout)

#reload eth2
result2= ("sudo ifdown eth2"
          "sudo ifup eth2")


