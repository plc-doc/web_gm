import re
import time

import flet
import subprocess

from httpx import request

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

current_eth0_ip = "ifconfig eth0| grep 'inet' | cut -d: -f2 | awk '{print $2}'"

# TODO:
#   ! IPv6 still does NOT work (can only read but no idea how to change)
#   ↓
#   main field must be in the center
#   show that interface is inactive
#   make white clouds wider
#   mb put interface name inside white cloud
#   ↓
#   class Users (login, logout)
#   ↓
#   icon to loading page and application icon


class Interface:
    def __init__(self, name, ip_6, mask, app, page):
        self.name = name
        self.ip_4 = self.get_ip4() #active ip from ifconfig
        self.ip_6 = self.get_ip6()
        self.mask = self.get_mask()
        self.mac_address = self.get_mac_address()
        self.gateway = self.get_gateway()
        self.app = app
        self.page = page
        self.dynamic = False #from configration file
        self.dynamic_ip6 = False

        self.ip_4_field = flet.Text(value=self.ip_4, color="black")
        self.mac_address_field = flet.Text(value=self.mac_address, color="black")
        self.ip_6_field = flet.Text(value=self.ip_6, color="black")

    def get_ip4(self):
        # result = subprocess.run(["ifconfig {self.name.lower()}| grep 'inet' | cut -d: -f2 | awk '{print $2}'"], shell=True,
        #                         capture_output=True, text=True, check=True)

        request = subprocess.run(["ip", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)

        output = request.stdout

        match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", output)
        if match:
            ip = match.group(1)

            return ip
        else:
            print("Not found")

    def get_ip6(self):
        request = subprocess.run(["ip", "-6", "addr", "show", self.name.lower()], capture_output=True, text=True, check=True)
        output = request.stdout

        match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)
        return match.group(1) if match else None

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

    def get_mask(self):
        result = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", self.name.lower()],
                                capture_output=True, text=True, check=True)
        output = result.stdout

        match = re.search(r"(/(\d+)\b)", output)
        if not match:
            return None

        cidr = int(match.group(1)[1:]) #cut first symbol "/"
        #Convertation - for example /24 -> 255.255.255.0
        mask = (0xffffffff << (32-cidr)) & 0xffffffff

        return ".".join(str((mask >> (8*i)) & 0xff) for i in reversed(range(4)))

    def get_gateway(self):
        in_block = False

        with open("/etc/network/interfaces", "r") as f:
            for line in f:
                # if line.strip().startswith("gateway"):
                #     return line.split()[1]

                if line.startswith(f"iface {self.name.lower()} inet static"):
                    in_block = True
                    continue
                if in_block:
                    if line.strip().startswith("gateway"):
                        return line.split()[1]
                    else:
                        continue

        return None

    def set_gateway(self):
        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"

        match = re.search(pattern, content, re.DOTALL)

        if not match:
            print("Block not found mask")

        eth_block = match.group(1)

        new_eth_block = re.sub(r"(^\s*gateway\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.gateway}", eth_block, flags=re.MULTILINE, count=1)

        new_content = content.replace(eth_block, new_eth_block)

        with open("/tmp/interfaces", "w") as f:
            f.write(new_content)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        #reload
        try:
            subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        except Exception:
            print("error mask")
        try:
            subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        except Exception:
            print("error2 mask")

    def set_mask(self):
        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"

        match = re.search(pattern, content, re.DOTALL)

        if not match:
            print("Block not found mask")

        eth_block = match.group(1)

        new_eth_block = re.sub(r"(^\s*netmask\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.mask}", eth_block, flags=re.MULTILINE, count=1)

        new_content = content.replace(eth_block, new_eth_block)

        with open("/tmp/interfaces", "w") as f:
            f.write(new_content)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        #reload
        try:
            subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        except Exception:
            print("error mask")
        try:
            subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        except Exception:
            print("error2 mask")


    def set_static_ip4(self):
        # subprocess.run(["sudo", 'ifconfig', 'eth0', '192.168.1.15', 'netmask', '255.255.255.0'])

        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        def repl(match: re.Match) -> str:
            mode = match.group(2)
            body = match.group(3)
            if mode == "dhcp":
                # switch to static
                header = f"iface {self.name.lower()} inet static"
                return "\n".join([
                    header,
                    f"      address {self.ip_4}\n"
                    f"      netmask {self.mask}\n"
                    f"      gateway {self.mac_address_field.value}\n"
                    f"      dns-nameservers 192.168.1.28 8.8.4.4\n"
                    f"      hwaddress ether {self.mac_address.value}\n"
                ]) + "\n"
            else:
                # keep static - change only address
                header = f"iface {self.name.lower()} inet static"
                # if found - change
                if re.search(r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)", body):
                    body = re.sub(
                        r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)",
                        rf"\g<1>{self.ip_4}",
                        body,
                        flags=re.MULTILINE
                    )
                # if not found - add
                else:
                    body =  f"      address {self.ip_4}\n" + body
                return header + body

        pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+(static|dhcp))([\s\S]*?)(?=^\s*iface|\Z)"
        new_content, count = re.subn(pattern, repl, content, flags=re.MULTILINE)

        if count == 0:
            raise RuntimeError("oups")

        '''block changing address for static ip'''
        # try:
        #     pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"
        # except AttributeError:
        #     pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+dhcp.*?)(?=(?:iface\s|\Z)"
        #
        # match = re.search(pattern, content, re.DOTALL)
        #
        # if not match:
        #     print("Block not found")
        #
        # eth_block = match.group(1)
        #
        # new_eth_block = re.sub(r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.ip_4}", eth_block, flags=re.MULTILINE, count=1)
        #
        # new_content = content.replace(eth_block, new_eth_block)

        with open("/tmp/interfaces", "w") as f:
            f.write(new_content)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        #reload
        try:
            subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        except Exception:
            print("error")
        try:
            subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        except Exception:
            print("error2")

    def set_dynamic_ip4(self):
        lines = []
        in_block = False

        with open("/etc/network/interfaces", "r") as f:
            for line in f:
                if line.startswith(f"iface {self.name.lower()} inet"):
                    lines.append(f"iface {self.name.lower()} inet dhcp\n")
                    in_block = True
                    continue
                if in_block:
                    if line.startswith("iface") or line.startswith("auto"):
                        in_block = False
                        lines.append(line)
                    else:
                        continue
                else:
                    lines.append(line)

        with open("/tmp/interfaces", "w") as f:
            f.writelines(lines)

        # old file copy
        with open("/tmp/interfaces2", "w") as f:
            f.writelines(lines)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        try:
            subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        except Exception:
            print("error")
        try:
            subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        except Exception:
            print("error2")


    def get_static_or_dynamic(self):
        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+(static|dhcp))([\s\S]*?)(?=\niface|\Z)"
        m = re.search(pattern, content, flags= re.MULTILINE)
        if not m:
            return None, None
        mode = m.group(2)

        if mode == "dhcp":
            self.dynamic = True

        return mode

    def get_static_or_dynamic_ip6(self):
        with open("/etc/network/interfaces", "r") as f:
        #     content = f.read()
        #
        # pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet6\s+static.*?)(?=(?:iface\s|\Z))"
        # m = re.search(pattern, content, flags= re.MULTILINE)
            for line in f:
                if line.startswith(f"iface {self.name.lower()} inet6 static"):
                    self.dynamic_ip6 = False
                    return "static"

        # if not m:
        request = subprocess.run(["ip", "-6", "addr", "show", self.name.lower()], capture_output=True, text=True,
                                 check=True)
        output = request.stdout

        match = re.search(r"inet6\s+([0-9a-f:]+)/\d+ scope", output)

        if match:
            self.dynamic_ip6 = True
            return "dhcp"
        else:
            return None

        # return match.group(1) if match else None

        # mode = m.group(2)
        #
        # if mode == "dhcp":
        #     self.dynamic_ip6 = True
        #
        # return mode



    def info_structure(self):
        return flet.Column(
            controls=[flet.Text(value=self.name, color="black"),
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
                                              )
                                              ],
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
                                                  icon_color="black"), ],
                                          alignment=flet.MainAxisAlignment.END,
                                      ),
                                  ],
                                  horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                  alignment=flet.MainAxisAlignment.CENTER,
                                  spacing=20
                              ),
                              width=282,
                              height=161,
                              padding=10,
                              bgcolor=white,
                              border_radius=20,
                          ),
                          color=white,
                          shadow_color="black",
                      ),
                      ],
            spacing=5,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.CENTER,
        )

    def open_ip_settings(self, e):
        global number

        def handle_button_save(e):
            self.ip_4 = ip_address_field.value
            self.ip_4_field.value = self.ip_4

            self.mask = mask_field.value

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

            self.mac_address = self.get_mac_address()
            self.mac_address_field.value = self.mac_address

            self.page.close(dialog)
            self.page.update()

        def handle_button_cancel(e):
            # ↓ ♥
            if self.dynamic:
                dropdown4.value = "Использовать DHCP"
            else:
                dropdown4.value = "Вручную"

            ip_address_field.value = self.ip_4
            ip_address_field.disabled = True
            mask_field.value = self.mask
            mask_field.disabled = True

            gateway_field.value = self.mac_address
            dropdown6.value = "Использовать DHCP"
            self.page.update()
            self.page.close(dialog)

        def ipv6_changed(e):

            selected = e.control.value
            print(selected)

            if selected == "Вручную":
                container.visible = True
                ip6_field.disabled = False
                ip6_field.value = self.ip_6
                mask6_field.disabled = False
                mask6_field.value = self.mask

            elif selected == "Использовать DHCP":
                container.visible = True
                ip6_field.disabled = True
                ip6_field.value = self.ip_6
                mask6_field.disabled = True
                mask6_field.value = self.mask
            else:
                container.visible = False
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
                # flet.dropdown.Option("Использовать BOOTP"),
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

        ip_address_field = flet.TextField(value = self.ip_4,bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                          cursor_color= orange, height=40, width=250, fill_color=white, text_size=14, disabled = False if dropdown4.value == "Вручную" else True)
        mask_field = flet.TextField(value = self.mask,bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14, disabled = False if dropdown4.value == "Вручную" else True)

        ip6_field = flet.TextField(value=self.ip_6, bgcolor=white, border_radius=14, focused_border_color=orange,
                                          selection_color=orange, color="black",
                                          cursor_color=orange, height=40, width=250, fill_color=white, text_size=14,
                                          disabled= False if dropdown6.value == "Вручную" else True)
        mask6_field = flet.TextField(value=self.mask, bgcolor=white, border_radius=14, focused_border_color=orange,
                                    selection_color=orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14,
                                    disabled= False if dropdown6.value == "Вручную" else True)

        container = flet.Container(
                            flet.Column([
                                flet.Row([
                                    flet.Column([
                                        flet.Text(value="IP-адрес", color="black"),
                                        flet.Text(value="Маска подсети", color="black")
                                    ]),
                                    flet.Column([
                                        ip6_field,
                                        mask6_field
                                    ])
                                ], spacing = 55)
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
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14)
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
                            flet.Text(value= "Сетевой шлюз", color= "black"),
                            gateway_field
                        ], alignment=flet.MainAxisAlignment.START, spacing = 85),
                        # flet.Row([
                        #     button_cancel,
                        #     button_save
                        # ], alignment=flet.MainAxisAlignment.END, spacing=30)

        ],
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        # alignment= flet.MainAxisAlignment.START,
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


