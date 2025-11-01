import re

import flet
import subprocess
import ipaddress
import yaml

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

current_eth0_ip = "ifconfig eth0| grep 'inet' | cut -d: -f2 | awk '{print $2}'"

# TODO:
#   mb put interface name inside white cloud

class Interface:
    def __init__(self, name, app, page, metric):
        self.name = name
        self.metric =  metric
        self.ip_4 = self.get_ip4() #active ip from ifconfig
        self.ip_6 = self.get_ip6()
        self.mask = self.get_mask()
        self.prefix_len = self.get_prefix_len()
        self.mac_address = self.get_mac_address()
        self.gateway = self.get_gateway()
        self.gateway6 = self.get_gateway6()
        self.app = app
        self.page = page
        self.dynamic = False #from configration file
        self.dynamic_ip6 = False
        self.static_ip6 = False

        self.ip_4_field = flet.Text(value=self.ip_4, color="black")
        self.mac_address_field = flet.Text(value=self.mac_address, color="black")
        self.ip_6_field = flet.Text(value=self.ip_6, color="black")

    def get_ip4(self):
        try:

            request = subprocess.run(["ip", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)

            output = request.stdout

            match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", output)
            if match:
                ip = match.group(1)

                return ip
            else:
                print("Not found")
                if not "state UP" in output:
                    with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                        config = yaml.safe_load(f)

                    ethernets = config.get("network", {}).get("ethernets", {})

                    for iface_name, iface_conf in ethernets.items():
                        dhcp = iface_conf.get("dhcp4", False)
                        addresses = iface_conf.get("addresses", [])

                        for address in addresses:
                            try:
                                if not dhcp:
                                    if iface_name == self.name.lower():
                                        print(address)
                                        ip, mask = address.split("/")

                                        if isinstance(ipaddress.ip_interface(address), ipaddress.IPv4Interface):
                                            print(f"ip, mask {self.name.lower()} ", ip, mask)
                                            return ip
                                else:
                                    print(self.name.lower(), " is dhcp")
                            except ValueError:
                                continue

                    return None
        except Exception:
            return ""

    def get_ip6(self):
        # try:
        #     request = subprocess.run(["ip", "-6", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)
        #     output = request.stdout
        #
        #     match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)
        #     return match.group(1) if match else None
        # except Exception:
        #     return ""

        try:
            request = subprocess.run(["ip","-6", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)

            output = request.stdout

            match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)
            if match:
                ip = match.group(1)
                return ip
            else:
                print("Not found")
                if not "state UP" in output:
                    with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                        config = yaml.safe_load(f)

                    ethernets = config.get("network", {}).get("ethernets", {})

                    for iface_name, iface_conf in ethernets.items():
                        dhcp = iface_conf.get("dhcp6", False)
                        addresses = iface_conf.get("addresses", [])

                        for address in addresses:
                            try:
                                if not dhcp:
                                    if iface_name == self.name.lower():
                                        print(address)
                                        ip, mask = address.split("/")

                                        if isinstance(ipaddress.ip_interface(address), ipaddress.IPv6Interface):
                                            print(f"ip, mask {self.name.lower()} ", ip, mask)
                                            return ip
                                else:
                                    print(self.name.lower(), " is dhcp")
                            except ValueError:
                                continue
                    return None
        except Exception:
            return ""

    def get_prefix_len(self):
        try:
            result = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", self.name.lower()],
                                    capture_output=True, text=True, check=True)
            output = result.stdout

            match = re.search(r"(/(\d+)\b)", output)

            if not match:
                if not "state UP" in output:
                    with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                        config = yaml.safe_load(f)

                    ethernets = config.get("network", {}).get("ethernets", {})

                    for iface_name, iface_conf in ethernets.items():
                        dhcp = iface_conf.get("dhcp6", False)
                        addresses = iface_conf.get("addresses", [])

                        for address in addresses:
                            try:
                                if not dhcp:
                                    if iface_name == self.name.lower():
                                        print(addresses[0])
                                        ip, prefix_len = addresses[0].split("/")

                                        if isinstance(ipaddress.ip_interface(address), ipaddress.IPv6Interface):
                                            print(f"ip, prefix_len {self.name.lower()} ", ip, prefix_len)
                                            return prefix_len
                                else:
                                    print(self.name.lower(), " is dhcp")
                            except ValueError:
                                continue
                    return ""
            return match.group(2)
        except Exception:
            return ""

    def get_mac_address(self):
        try:
            result = subprocess.run(['ip', 'link', 'show', self.name.lower()], capture_output=True, text=True, check=True)
            output = result.stdout

            match = re.search(r"link/ether\s+([0-9a-f:]{17})", output)
            if match:
                return match.group(1)
            else:
                return None
        except subprocess.CalledProcessError:
            return None
        except Exception:
            return ""

    def get_mask(self):
        try:
            result = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", self.name.lower()],
                                    capture_output=True, text=True, check=True)
            output = result.stdout

            match = re.search(r"(/(\d+)\b)", output)

            if not match:
                if not "state UP" in output:
                    with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                        config = yaml.safe_load(f)

                    ethernets = config.get("network", {}).get("ethernets", {})

                    for iface_name, iface_conf in ethernets.items():
                        dhcp = iface_conf.get("dhcp4", False)
                        addresses = iface_conf.get("addresses", [])

                        if not dhcp:
                            if iface_name == self.name.lower():
                                print(addresses[0])
                                ip, mask = addresses[0].split("/")

                                print(f"ip, mask {self.name.lower()} ", ip, mask)
                                return str(ipaddress.IPv4Network(f"0.0.0.0/{mask}").netmask)
                        else:
                            print(self.name.lower(), " is dhcp")

            cidr = int(match.group(1)[1:]) #cut first symbol "/"
            #Convertation - for example /24 -> 255.255.255.0
            mask = (0xffffffff << (32-cidr)) & 0xffffffff

            return ".".join(str((mask >> (8*i)) & 0xff) for i in reversed(range(4)))
        except Exception:
            return ""

    def get_up_down(self):
        try:
            result = subprocess.run(["ip", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)
            output = result.stdout

            if "state UP" in output:
                return True
            else:
                return False

        except subprocess.CalledProcessError as e:
            print(e)
            return False

    def get_gateway6(self):
        try:
            with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                data = yaml.safe_load(f)

            iface_data = data.get("network", {}).get("ethernets", {})
            routes = iface_data[self.name.lower()].get("routes", [])

            print(routes)

            for r in routes:
                print(r.get("to"))
                if r.get("to") == "::/0":
                    return str(r.get("via"))
            return None

        except Exception as e:
            print(e)
            return None

    def get_gateway(self):
        # in_block = False
        #
        # try:
        #     with open("/etc/network/interfaces", "r") as f:
        #         for line in f:
        #             # if line.strip().startswith("gateway"):
        #             #     return line.split()[1]
        #
        #             if line.startswith(f"iface {self.name.lower()} inet static"):
        #                 in_block = True
        #                 continue
        #             if in_block:
        #                 if line.strip().startswith("gateway"):
        #                     return line.split()[1]
        #                 else:
        #                     continue
        #
        #     return None
        # except Exception:
        #     return ""

        try:
            with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                data = yaml.safe_load(f)

            iface_data = data.get("network", {}).get("ethernets", {})
            routes = iface_data[self.name.lower()].get("routes", [])

            print(routes)

            for r in routes:
                print(r.get("to"))
                if r.get("to") == "0.0.0.0/0":
                    return str(r.get("via"))

            return None

        except Exception as e:
            print(e)
            return None

    def set_gateway(self):
        # with open("/etc/network/interfaces", "r") as f:
        #     content = f.read()
        #
        # pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"
        #
        # match = re.search(pattern, content, re.DOTALL)
        #
        # if not match:
        #     print("Block not found mask")
        #
        # eth_block = match.group(1)
        #
        # new_eth_block = re.sub(r"(^\s*gateway\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.gateway}", eth_block, flags=re.MULTILINE, count=1)
        #
        # new_content = content.replace(eth_block, new_eth_block)
        #
        # with open("/tmp/interfaces", "w") as f:
        #     f.write(new_content)
        #
        # subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)
        #
        # #reload
        # try:
        #     subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        # except Exception:
        #     print("error mask")
        # try:
        #     subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        # except Exception:
        #     print("error2 mask")

        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        target_key = None
        for key, value in ethernets.items():
            if value.get("set_name", "").lower() == self.name.lower() or key.lower() == self.name.lower():
                target_key = key
                break
        if not target_key:
            raise ValueError(f"Interface '{self.name.lower()} not found in netplan file")

        iface_conf = ethernets[target_key]

        iface_conf["routes"] = [{"to": "0.0.0.0/0", "via": self.gateway}]

        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(["sudo", "netplan", "apply"], check=True)

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

        print("copied gateway")


    def set_mask(self):
        def set_netmask(interface, new_prefix, netplan_file = "/etc/netplan/50-cloud-init.yaml"):
            with open(netplan_file, "r") as f:
                config = yaml.safe_load(f)

            ethernets = config.get("network", {}).get("ethernets", {})
            print(ethernets)
            if interface not in ethernets:
                raise ValueError(f'interface not found in netplan file')

            addresses = ethernets[interface].get("addresses", [])
            print(ethernets[interface])
            if not addresses:
                raise ValueError("interface has no addresses")

            ip_cidr = addresses[0]
            ip_only = ip_cidr.split("/")[0]
            new_ip_cidr = f"{ip_only}/{new_prefix}"

            ethernets[interface]["addresses"][0] = new_ip_cidr

            with open(netplan_file, "w") as f:
                yaml.safe_dump(config, f, default_flow_style=False)

            subprocess.run(["sudo", "netplan", "apply"], check=True)

        set_netmask(self.name.lower(), ipaddress.IPv4Network(f'0.0.0.0/{self.mask}').prefixlen)

        # def change_netmask(interface, new_prefix, yaml_file="/usr/local/bin/interfaces_backup"):
        #     subprocess.run(["sed", "-i", rf"/{interface}/,/^[^ ]/ s|\(/.*\)/[0-9]\+|\1/{new_prefix}|", yaml_file], check=True)
        #
        # change_netmask(self.name.lower(), ipaddress.IPv4Network(f'0.0.0.0/{self.mask}').prefixlen, "/usr/local/bin/interfaces_backup")

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

        print("copied mask")

    # def set_mask(self):
    #     with open("/etc/network/interfaces", "r") as f:
    #         content = f.read()
    #
    #     pattern = rf"{re.escape(self.name.lower())}"
    #
    #     match = re.search(pattern, content, re.DOTALL)
    #
    #     if not match:
    #         print("Block not found mask")
    #
    #     eth_block = match.group(1)
    #
    #     new_eth_block = re.sub(r"(^\s*netmask\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.mask}", eth_block, flags=re.MULTILINE, count=1)
    #
    #     new_content = content.replace(eth_block, new_eth_block)
    #
    #     with open("/tmp/interfaces", "w") as f:
    #         f.write(new_content)
    #
    #     subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)
    #
    #     #reload
    #     try:
    #         subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
    #     except Exception:
    #         print("error mask")
    #     try:
    #         subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
    #     except Exception:
    #         print("error2 mask")

    def turn_off_ip6(self):
        def is_ipv6_address(address):
            try:
                ip = ipaddress.ip_interface(address)
                return isinstance(ip, ipaddress.IPv6Interface)
            except ValueError:
                return False

        def is_ipv6_route(route):
            try:
                ip = ipaddress.ip_network(route['to'])
                return ip.version == 6
            except (KeyError, ValueError):
                return False

        def remove_ipv6_addresses(addresses):
            return [addr for addr in addresses if not is_ipv6_address(addr)]

        def remove_ipv6_routes(routes):
            return [route for route in routes if not is_ipv6_route(route)]

        # Загрузка YAML
        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        for iface, settings in ethernets.items():
            if iface == self.name.lower():
                # Отключить DHCPv6 и RA
                settings["dhcp6"] = False
                settings["accept-ra"] = False

                # Удалить IPv6-адреса
                if "addresses" in settings:
                    settings["addresses"] = remove_ipv6_addresses(settings["addresses"])
                    if not settings["addresses"]:
                        del settings["addresses"]

                # Удалить IPv6-маршруты
                if "routes" in settings:
                    settings["routes"] = remove_ipv6_routes(settings["routes"])
                    if not settings["routes"]:
                        del settings["routes"]

        # Сохранение результата
        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(['sudo', 'netplan', 'apply'], check = True)

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()
            print(content)

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)


    def set_dynamic_ip6(self):

        def is_ipv6_address(address):
            try:
                ip = ipaddress.ip_interface(address)
                return isinstance(ip, ipaddress.IPv6Interface)
            except ValueError:
                return False

        def is_ipv6_route(route):
            try:
                ip = ipaddress.ip_network(route['to'])
                return ip.version == 6
            except (KeyError, ValueError):
                return False

        def filter_ipv6_addresses(addresses):
            return [addr for addr in addresses if not is_ipv6_address(addr)]

        def filter_ipv6_routes(routes):
            return [route for route in routes if not is_ipv6_route(route)]

        # Загрузка YAML
        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        for iface, settings in ethernets.items():
            # Включить DHCP для IPv6
            if iface == self.name.lower():
                settings["dhcp6"] = True

                # Удалить только IPv6 адреса
                if "addresses" in settings:
                    settings["addresses"] = filter_ipv6_addresses(settings["addresses"])
                    if not settings["addresses"]:
                        del settings["addresses"]

                # Удалить только IPv6 маршруты
                if "routes" in settings:
                    settings["routes"] = filter_ipv6_routes(settings["routes"])
                    if not settings["routes"]:
                        del settings["routes"]

        # Сохранение результата
        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(['sudo', 'netplan', 'apply'], check = True)

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()
            print(content)

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

    def set_static_ip6(self):
        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        target_key = None
        for key, value in ethernets.items():
            if key.lower() == self.name.lower() or value.get("set_name", "").lower() == self.name.lower():
                target_key = key
                break
        if not target_key:
            raise ValueError(f"interface {self.name.lower()} not found in yaml")

        iface = ethernets[target_key]

        print(iface)

        ipv4, ipv6 = [], []
        addresses = iface.get("addresses", [])
        for addr in addresses:
            try:
                ip = ipaddress.ip_interface(addr)
                if isinstance(ip, ipaddress.IPv4Interface):
                    ipv4.append(addr)
                else:
                    ipv6.append(addr)
            except ValueError:
                continue

        if ipv6:
            ipv6 = [f'{self.ip_6}/{self.prefix_len}']
        else:
            ipv6.append(f'{self.ip_6}/{self.prefix_len}')

        iface["dhcp6"] = False
        # iface["addresses"] = [f'{self.ip_4}/{ipaddress.IPv4Network(f"0.0.0.0/{self.mask}").prefixlen}']
        iface['addresses'] = ipv4 + ipv6

        for route in iface["routes"]:
            if route not in [{"to": "::/0", "via": self.gateway6}]:
                if not iface["dhcp4"]:
                    iface["routes"].append({"to": "::/0", "via": self.gateway6})
                else:
                    iface["routes"] = [{"to": "::/0", "via": self.gateway6}]

        if self.name.lower() == "eth0":
            for ns in iface['nameservers'].get('addresses', []):
                if ns not in ["8.8.8.8", "8.8.4.4", "2001:4860:4860::8888", "2001:4860:4860::8844"]:
                    iface["nameservers"].append("2001:4860:4860::8888", "2001:4860:4860::8844")

        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(['sudo', 'netplan', 'apply'], check = True)

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()
            print(content)

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

        print("copied static ip6")


    def set_static_ip4(self):
        # subprocess.run(["sudo", 'ifconfig', 'eth0', '192.168.1.15', 'netmask', '255.255.255.0'])

        # with open("/etc/network/interfaces", "r") as f:
        #     content = f.read()
        #
        # def repl(match: re.Match) -> str:
        #     mode = match.group(2)
        #     body = match.group(3)
        #     if mode == "dhcp":
        #         # switch to static
        #         header = f"iface {self.name.lower()} inet static"
        #         return "\n".join([
        #             header,
        #             f"      address {self.ip_4}\n"
        #             f"      netmask {self.mask}\n"
        #             f"      gateway {self.gateway}\n"
        #             f"      dns-nameservers 192.168.1.28 8.8.4.4\n"
        #             f"      hwaddress ether {self.mac_address.value}\n"
        #         ]) + "\n"
        #     else:
        #         # keep static - change only address
        #         header = f"iface {self.name.lower()} inet static"
        #         # if found - change
        #         if re.search(r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)", body):
        #             body = re.sub(
        #                 r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)",
        #                 rf"\g<1>{self.ip_4}",
        #                 body,
        #                 flags=re.MULTILINE
        #             )
        #         # if not found - add
        #         else:
        #             body =  f"      address {self.ip_4}\n" + body
        #         return header + body
        #
        # pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+(static|dhcp))([\s\S]*?)(?=^\s*iface|\Z)"
        # new_content, count = re.subn(pattern, repl, content, flags=re.MULTILINE)
        #
        # if count == 0:
        #     raise RuntimeError("oups")
        #
        # '''block changing address for static ip'''
        # # try:
        # #     pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"
        # # except AttributeError:
        # #     pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+dhcp.*?)(?=(?:iface\s|\Z)"
        # #
        # # match = re.search(pattern, content, re.DOTALL)
        # #
        # # if not match:
        # #     print("Block not found")
        # #
        # # eth_block = match.group(1)
        # #
        # # new_eth_block = re.sub(r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.ip_4}", eth_block, flags=re.MULTILINE, count=1)
        # #
        # # new_content = content.replace(eth_block, new_eth_block)
        #
        # with open("/tmp/interfaces", "w") as f:
        #     f.write(new_content)
        #
        # subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)
        #
        # #reload
        # try:
        #     subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        # except Exception:
        #     print("error")
        # try:
        #     subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        # except Exception:
        #     print("error2")

        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        target_key = None
        for key, value in ethernets.items():
            if key.lower() == self.name.lower() or value.get("set_name", "").lower() == self.name.lower():
                target_key = key
                break
        if not target_key:
            raise ValueError(f"interface {self.name.lower()} not found in yaml")

        iface = ethernets[target_key]

        print(iface)

        ipv4, ipv6 = [], []
        addresses = iface.get("addresses", [])
        for addr in addresses:
            try:
                ip = ipaddress.ip_interface(addr)
                if isinstance(ip, ipaddress.IPv4Interface):
                    ipv4.append(addr)
                else:
                    ipv6.append(addr)
            except ValueError:
                continue

        if ipv4:
            ipv4 = [f'{self.ip_4}/{ipaddress.IPv4Network(f"0.0.0.0/{self.mask}").prefixlen}']
        else:
            ipv4.append(f'{self.ip_4}/{ipaddress.IPv4Network(f"0.0.0.0/{self.mask}").prefixlen}')

        iface["dhcp4"] = False
        # iface["addresses"] = [f'{self.ip_4}/{ipaddress.IPv4Network(f"0.0.0.0/{self.mask}").prefixlen}']
        iface['addresses'] = ipv4 + ipv6
        iface["routes"] = [{"to": "0.0.0.0/0", "via": self.gateway, "metric": self.metric}]

        if self.name.lower() == "eth0":
            iface["nameservers"] = {"addresses":["8.8.8.8", "8.8.4.4"]}

        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(['sudo', 'netplan', 'apply'], check = True)

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()
            print(content)

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

        print("copied static ip4")

    def set_dynamic_ip4(self):
        # lines = []
        # in_block = False

        # with open("/etc/network/interfaces", "r") as f:
        #     for line in f:
        #         if line.startswith(f"iface {self.name.lower()} inet"):
        #             lines.append(f"iface {self.name.lower()} inet dhcp\n")
        #             in_block = True
        #             continue
        #         if in_block:
        #             if line.startswith("iface") or line.startswith("auto"):
        #                 in_block = False
        #                 lines.append(line)
        #             else:
        #                 continue
        #         else:
        #             lines.append(line)
        #
        # with open("/tmp/interfaces", "w") as f:
        #     f.writelines(lines)
        #
        # # old file copy
        # with open("/tmp/interfaces2", "w") as f:
        #     f.writelines(lines)
        #
        # subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)
        #
        # try:
        #     subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        # except Exception:
        #     print("error")
        # try:
        #     subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        # except Exception:
        #     print("error2")

        def is_ipv4_address(address):
            try:
                ip = ipaddress.ip_interface(address)
                return isinstance(ip, ipaddress.IPv4Interface)
            except ValueError:
                return False

        def is_ipv4_route(route):
            try:
                ip = ipaddress.ip_network(route['to'])
                return ip.version == 4
            except (KeyError, ValueError):
                return False

        def filter_ipv4_addresses(addresses):
            return [addr for addr in addresses if not is_ipv4_address(addr)]

        def filter_ipv4_routes(routes):
            return [route for route in routes if not is_ipv4_route(route)]

        # Загрузка YAML
        with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
            config = yaml.safe_load(f)

        ethernets = config.get("network", {}).get("ethernets", {})

        for iface, settings in ethernets.items():
            if iface == self.name.lower():

                # Включить DHCP для IPv4
                settings["dhcp4"] = True

                # Удалить только IPv4 адреса
                if "addresses" in settings:
                    settings["addresses"] = filter_ipv4_addresses(settings["addresses"])
                    if not settings["addresses"]:
                        del settings["addresses"]

                # Удалить только IPv4 маршруты
                if "routes" in settings:
                    settings["routes"] = filter_ipv4_routes(settings["routes"])
                    if not settings["routes"]:
                        del settings["routes"]

        with open("/etc/netplan/50-cloud-init.yaml", "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

        subprocess.run(['sudo', 'netplan', 'apply'], check = True)

        print("successfully")

        with open("/etc/netplan/50-cloud-init.yaml", "r") as src_file:
            content = src_file.read()

        with open("/usr/local/bin/interfaces_backup", "w") as backup_file:
            backup_file.write(content)

    def get_static_or_dynamic(self):
        global mode
        try:
        #     with open("/etc/network/interfaces", "r") as f:
        #         content = f.read()
        #
        #     pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+(static|dhcp))([\s\S]*?)(?=\niface|\Z)"
        #     m = re.search(pattern, content, flags= re.MULTILINE)
        #     if not m:
        #         return None, None
        #     mode = m.group(2)
        #
        #     if mode == "dhcp":
        #         self.dynamic = True
        #
        #     return mode
        # except Exception:
        #     return ""
            with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                config = yaml.safe_load(f)

            ethernets = config.get("network", {}).get("ethernets", {})

            for iface_name, iface_conf in ethernets.items():
                dhcp = iface_conf.get("dhcp4", False)
                addresses = iface_conf.get("addresses", [])

                if dhcp:
                    if iface_name == self.name.lower():
                        print("equal")
                        self.dynamic = True
                        mode = "dhcp"
                        break
                    # else:
                    #     print("iface_name not equal self.name")
                    #     self.dynamic = True
                    #     mode = "dhcp"
                else:
                    if iface_name == self.name.lower():
                        mode = "static"
                        break
            return mode

        except Exception:
            return ""

    def get_static_or_dynamic_ip6(self):
        # try:
        #     with open("/etc/network/interfaces", "r") as f:
        #
        #         for line in f:
        #             if line.startswith(f"iface {self.name.lower()} inet6 static"):
        #                 self.dynamic_ip6 = False
        #                 return "static"
        #
        #     # if not m:
        #     request = subprocess.run(["ip", "-6", "addr", "show", self.name.lower()], capture_output=True, text=True,
        #                              check=True)
        #     output = request.stdout
        #
        #     match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)
        #
        #     if match:
        #         self.dynamic_ip6 = True
        #         return "dhcp"
        #     else:
        #         return None
        # except Exception:
        #     return ""
        global mode6
        try:
            with open("/etc/netplan/50-cloud-init.yaml", "r") as f:
                config = yaml.safe_load(f)

            ethernets = config.get("network", {}).get("ethernets", {})

            for iface_name, iface_conf in ethernets.items():
                dhcp = iface_conf.get("dhcp6", False)
                addresses = iface_conf.get("addresses", [])

                if dhcp:
                    if iface_name == self.name.lower():
                        print("equal")
                        self.dynamic_ip6 = True
                        self.static_ip6 = False
                        mode6 = "dhcp"
                        break
                    # else:
                    #     print("iface_name not equal self.name")
                    #     self.dynamic = True
                    #     mode = "dhcp"
                elif "dhcp6" not in iface_conf:
                    if iface_name == self.name.lower():
                        try:
                            request = subprocess.run(["ip", "-6", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)
                            output = request.stdout

                            match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)
                            if match:
                                self.dynamic_ip6 = True
                                self.static_ip6 = False
                                mode6 = "dhcp"
                                break
                            else:
                                self.static_ip6 = False
                                self.dynamic_ip6 = False
                                mode6 = "off"
                                break
                        except Exception:
                            continue
                elif not iface_conf.get("accept-ra"):
                    self.static_ip6 = False
                    self.dynamic_ip6 = False
                    mode6 = "off"
                    break
                else:
                    if iface_name == self.name.lower():
                        self.static_ip6 = True
                        self.dynamic_ip6 = False
                        mode6 = "static"
                        break
            return mode6

        except Exception:
            return ""


    # Eth (i) white clouds layout
    def info_structure(self):
        return flet.Column(
            controls=[flet.Row(controls=[flet.Text(value=self.name, color="black"),
                                         flet.Icon(name=flet.Icons.CIRCLE,
                                                   color="#0AA557" if self.get_up_down() else "#A0A0A0",
                                                   size=15,
                                         ),],
                               spacing=3,
                               alignment=flet.MainAxisAlignment.CENTER,
                               vertical_alignment=flet.CrossAxisAlignment.CENTER,
                               ),
                      flet.Card(
                          content=flet.Container(
                              content=flet.Column(
                                  controls=[
                                      flet.Row(
                                          controls=
                                              [flet.Column(
                                                  controls=[
                                                      flet.Text(value="IP-адрес(IPv4)", color="black"),
                                                      flet.Text(value="mac адрес", color="black"),
                                                      flet.Text(value="IP-адрес(IPv6)", color="black")],
                                                  horizontal_alignment=flet.CrossAxisAlignment.START
                                              ),
                                              flet.Column(
                                                  controls=[
                                                      self.ip_4_field,
                                                      self.mac_address_field,
                                                      self.ip_6_field],
                                                  alignment=flet.MainAxisAlignment.START,
                                              )],
                                          alignment=flet.MainAxisAlignment.CENTER,
                                          spacing=40,
                                      ),
                                      flet.Row(
                                          controls=[
                                              flet.FilledTonalButton(
                                                  text="Настроить",
                                                  icon=flet.Icons.SETTINGS,
                                                  bgcolor=orange,
                                                  color="black",
                                                  on_click=self.open_ip_settings,
                                                  icon_color="black"),
                                          ],alignment=flet.MainAxisAlignment.END,
                                      ),
                                  ],
                                  horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                  alignment=flet.MainAxisAlignment.CENTER,
                                  spacing=20
                              ),
                              width=300,
                              height=161,
                              padding=10,
                              bgcolor=white,
                              border_radius=12,
                              expand=True,
                              # animate_size=flet.Animation(600, flet.AnimationCurve.LINEAR),
                              on_hover=self.on_hover,
                          ),
                          color=white,
                          shadow_color="black",
                      ),],
            spacing=5,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.CENTER,
            expand = True
        )

    def on_hover(self, e):
        e.control.shadow = flet.BoxShadow(color="#AAAAAA",
                                          offset=flet.Offset(-1,7),
                                          blur_radius=4, spread_radius=1) if e.data == "true" else None
        # e.control.width = 302 if e.data == "true" else 300
        # e.control.height = 163 if e.data == "true" else 161

        e.control.update()

    # Eth (i) settings
    # opening dialog
    def open_ip_settings(self, e):
        global number

        def handle_button_save(e):

            #checking correctness of input values
            if dropdown4.value == "Вручную":
                try:
                    isinstance(ipaddress.ip_interface(ip_address_field.value), ipaddress.IPv4Interface)
                except ValueError:
                    ip_address_field.error_text = "Неверный IP-адрес"
                    return

                try:
                    isinstance(ipaddress.ip_interface(mask_field.value), ipaddress.IPv4Interface)
                except ValueError:
                    mask_field.error_text = "Неверное значение маски"
                    return

                try:
                    isinstance(ipaddress.ip_interface(gateway_field.value), ipaddress.IPv4Interface)
                except ValueError:
                    gateway_field.error_text = "Неверное значение сетевого шлюза"
                    return

            if dropdown6.value == "Вручную":
                try:
                    isinstance(ipaddress.ip_interface(ip6_field.value), ipaddress.IPv6Interface)
                except ValueError:
                    ip6_field.error_text = "Неверное значение IP"
                    return

                try:
                    isinstance(prefixlen_field.value, int)
                except ValueError:
                    prefixlen_field.error_text = "Неверное значение длины префикса"
                    return

                try:
                    isinstance(ipaddress.ip_interface(gateway6_field.value), ipaddress.IPv6Interface)
                except ValueError:
                    gateway6_field.error_text = "Неверное значение сетевого шлюза"
                    return

            self.ip_4 = ip_address_field.value
            self.ip_4_field.value = self.ip_4
            self.mask = mask_field.value
            self.gateway = gateway_field.value
            self.ip_6 = ip6_field.value
            self.ip_6_field.value = self.ip_6
            self.prefix_len = prefixlen_field.value
            self.gateway6 = gateway6_field.value

            e.control.visible = False
            button_cancel.visible = False

            if dropdown4.value == "Вручную":
                self.set_static_ip4()
                self.set_mask()
                self.set_gateway()
                # self.mask = self.get_mask()
                # mask_field.value = self.mask
            elif dropdown4.value == "Использовать DHCP":
                self.set_dynamic_ip4()
                self.ip_4 = self.get_ip4()
                self.ip_4_field.value = self.ip_4

            if dropdown6.value == "Вручную":
                self.set_static_ip6()
                self.ip_6 = self.get_ip6()
                self.ip_6_field.value = self.ip_6
            elif dropdown6.value == "Использовать DHCP":
                self.set_dynamic_ip6()
                self.ip_6 = self.get_ip6()
                self.ip_6_field.value = self.ip_6
            elif dropdown6.value == "Отключено":
                self.turn_off_ip6()
                self.ip_6 = self.get_ip6()
                self.ip_6_field.value = self.ip_6

            self.gateway = self.get_gateway()
            gateway_field.value = self.gateway

            self.gateway6 = self.get_gateway6()
            gateway6_field.value = self.gateway6

            self.prefix_len = self.get_prefix_len()
            prefixlen_field.value = self.prefix_len

            self.page.close(dialog)
            snackbar = flet.SnackBar(flet.Text("Изменения сохранены"))
            e.control.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

        def handle_button_cancel(e):
            # ↓ ♥
            if self.dynamic:
                dropdown4.value = "Использовать DHCP"
            else:
                dropdown4.value = "Вручную"

            if self.dynamic_ip6:
                dropdown6.value = "Использовать DHCP"
            elif self.static_ip6:
                dropdown6.value = "Вручную"
            else:
                dropdown6.value = "Отключено"

            ip_address_field.value = self.ip_4
            ip_address_field.disabled = True
            mask_field.value = self.mask
            mask_field.disabled = True

            gateway_field.value = self.gateway
            gateway6_field.value = self.gateway6
            dropdown6.value = "Использовать DHCP"
            self.page.update()
            self.page.close(dialog)

        def ipv6_changed(e):

            selected = e.control.value
            print(selected)

            if selected == "Вручную":
                container.visible = True
                gateway6_field.visible = True
                fields.controls[3].controls[1].controls[0].visible = True
                ip6_field.disabled = False
                ip6_field.value = self.ip_6
                prefixlen_field.disabled = False
                prefixlen_field.value = self.prefix_len
                gateway6_field.disabled = False
                gateway6_field.value = self.gateway6

            elif selected == "Использовать DHCP":
                container.visible = True
                gateway6_field.visible = True
                fields.controls[3].controls[1].controls[0].visible = True
                ip6_field.disabled = True
                ip6_field.value = self.ip_6
                prefixlen_field.disabled = True
                prefixlen_field.value = self.prefix_len
                gateway6_field.disabled = True
                gateway6_field.value = self.gateway6

            else:
                container.visible = False
                gateway6_field.visible = False
                fields.controls[3].controls[1].controls[0].visible = False
            self.page.update()

        def ipv4_changed(e):
            selected = e.control.value
            print(selected)

            if selected == "Вручную":
                ip_address_field.disabled = False
                ip_address_field.value = self.ip_4
                mask_field.disabled = False
                mask_field.value = self.mask
                gateway_field.disabled = False
                gateway_field.value = self.gateway

            else:
                ip_address_field.disabled = True
                ip_address_field.value = self.ip_4
                mask_field.disabled = True
                mask_field.value = self.mask
                gateway_field.disabled = True
                gateway_field.value = self.gateway
            self.page.update()

        dropdown4 = flet.Dropdown(
            value="Использовать DHCP" if self.get_static_or_dynamic() == "dhcp" else "Вручную",
            width=240,
            options=[
                flet.dropdown.Option("Использовать DHCP"),
                flet.dropdown.Option("Вручную")
            ],
            border_radius=10,
            color="black",
            text_size=14,
            bgcolor=orange,
            border_color="black",
            focused_border_color=orange,
            on_change=ipv4_changed,
        )

        def get_dropdown6_value():
            value = self.get_static_or_dynamic_ip6()

            if value == "dhcp":
                return "Использовать DHCP"
            elif value == "static":
                return "Вручную"
            else:
                return "Отключено"

        dropdown6 = flet.Dropdown(
            value= get_dropdown6_value(),
            width=240,
            options=[
                flet.dropdown.Option("Отключено"),
                flet.dropdown.Option("Использовать DHCP"),
                flet.dropdown.Option("Вручную"),
            ],
            border_radius=10,
            color="black",
            text_size=14,
            bgcolor=orange,
            border_color="black",
            focused_border_color=orange,
            on_change=ipv6_changed
        )

        def on_click(a):
            a.control.error_text = None
            self.page.update()


        ip_address_field = flet.TextField(value = self.ip_4,bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                          cursor_color= orange, height=40, width=250, fill_color=white, text_size=14, disabled = False if dropdown4.value == "Вручную" else True, on_click=on_click)
        mask_field = flet.TextField(value = self.mask,bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14, disabled = False if dropdown4.value == "Вручную" else True, on_click=on_click)

        ip6_field = flet.TextField(value=self.ip_6, bgcolor=white, border_radius=14, focused_border_color=orange,
                                          selection_color=orange, color="black",
                                          cursor_color=orange, height=40, width=250, fill_color=white, text_size=14,
                                          disabled= False if dropdown6.value == "Вручную" else True, on_click=on_click)
        prefixlen_field = flet.TextField(value=self.prefix_len, bgcolor=white, border_radius=14, focused_border_color=orange,
                                    selection_color=orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14,
                                    disabled= False if dropdown6.value == "Вручную" else True, on_click=on_click)
        gateway6_field = flet.TextField(value=self.gateway6, bgcolor=white, border_radius=14, focused_border_color=orange,
                                    selection_color=orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14,
                                    disabled= False if dropdown6.value == "Вручную" else True,
                                    visible = False if dropdown6.value == "Отключено" else True, on_click=on_click)

        container = flet.Container(
                            flet.Column([
                                flet.Row([
                                    flet.Column([
                                        flet.Text(value="IP-адрес", color="black"),
                                        flet.Text(value="Длина префикса", color="black"),
                                        #flet.Text(value="Сетевой шлюз", color="black")
                                    ]),
                                    flet.Column([
                                        ip6_field,
                                        prefixlen_field,
                                        #gateway6_field
                                    ])
                                ])
                            ]),
                            visible = False if dropdown6.value == "Отключено" else True
        )
        container_4 = flet.Container(
                            flet.Column([
                                flet.Row([
                                    flet.Column([
                                        flet.Text(value="IP-адрес", color="black"),
                                        flet.Text(value="Маска подсети", color="black")
                                    ]),
                                    flet.Column([
                                        ip_address_field,
                                        mask_field
                                    ])
                                ], spacing = 55)
                            ])
        )

        gateway_field = flet.TextField(value=self.gateway, bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14, disabled = False if dropdown4.value == "Вручную" else True, on_click=on_click)
        button_cancel = flet.ElevatedButton(text="Отменить изменения", color=orange, bgcolor="white", width=209,
                                            height=28, on_click=handle_button_cancel, )
        button_save = flet.ElevatedButton(text="Применить", color="black", bgcolor=orange, width=137, height=28,
                                          on_click=handle_button_save, disabled = False)

        fields = flet.Column([
                        flet.Text(value= self.name, color="black"),
                        flet.Row([
                            flet.Row([
                                flet.Text(value= "Конфигурация IPv4", color= "black"),
                                dropdown4,
                                ],spacing= 30,),
                            flet.Row([
                                flet.Text(value= "Конфигурация IPv6", color= "black"),
                                dropdown6,
                            ],spacing= 30,),
                        ],alignment=flet.MainAxisAlignment.CENTER,spacing= 100),
                        flet.Row([container_4, container], alignment= flet.MainAxisAlignment.SPACE_BETWEEN, spacing= 85), #Появляющееся окно ручной настройки
                        flet.Row([
                            flet.Row([
                                flet.Text(value= "Сетевой шлюз", color= "black"),
                                gateway_field], spacing=60),
                            flet.Row([
                                flet.Text(value= "Сетевой шлюз", color= "black", visible = False if dropdown6.value == "Отключено" else True),
                                gateway6_field], spacing=27)
                        ], alignment= flet.MainAxisAlignment.SPACE_BETWEEN, spacing = 85),
                        # flet.Row([
                        #     button_cancel,
                        #     button_save
                        # ], alignment=flet.MainAxisAlignment.END, spacing=30)

        ],
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        alignment= flet.MainAxisAlignment.SPACE_BETWEEN,
        spacing = 30,
        # width=100,
        height=270,
        )

        dialog_field =(
            flet.Column(controls=[
                fields,
                flet.Row([
                    button_cancel,
                    button_save
                ], alignment=flet.MainAxisAlignment.END, spacing=30)
            ],
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            spacing= 40
            )
        )

        dialog = flet.AlertDialog(
            content=flet.Container(
                width=900,
                height=350,
                content=dialog_field
            ),
            bgcolor=white,
            on_dismiss=lambda e: print("Dialog dismissed!"),
            content_padding=50,
        )

        self.page.open(dialog)
        dialog.open = True
        self.page.update()
        # dialog_text.focus()


