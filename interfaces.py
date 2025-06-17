import re

import flet
import subprocess

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

current_eth0_ip = "ifconfig eth0| grep 'inet' | cut -d: -f2 | awk '{print $2}'"

class Interface:
    def __init__(self, name, ip_6, mask, app, page):
        self.name = name
        self.ip_4 = self.get_ip4() #active ip from ifconfig
        self.ip_6 = ip_6
        self.mask = mask
        self.mac_address = "00:1A:2B:3C"
        self.app = app
        self.page = page
        self.dynamic = False #from configration file

        self.ip_4_field = flet.Text(value=self.ip_4, color="black")
        self.mac_address_field = flet.Text(value=self.mask, color="black")
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


    def set_static_ip4(self):
        # subprocess.run(["sudo", 'ifconfig', 'eth0', '192.168.1.15', 'netmask', '255.255.255.0'])

        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        # if self.name == "Eth0":
        #     eth_block_match = re.search(r"(auto\s+eth0.*?)(?=auto|\Z)", content, re.DOTALL)
        # if self.name == "Eth1":
        #     eth_block_match = re.search(r"(auto\s+eth1.*?)(?=auto|\Z)", content, re.DOTALL)
        # if self.name == "Eth2":
        #     eth_block_match = re.search(r"(auto\s+eth2.*?)(?=auto|\Z)", content, re.DOTALL)
        # if self.name == "Eth3":
        #     eth_block_match = re.search(r"(auto\s+eth3.*?)(?=auto|\Z)", content, re.DOTALL)

        try:
            pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+static.*?)(?=(?:iface\s|\Z))"
        except AttributeError:
            pattern = rf"(iface\s+{re.escape(self.name.lower())}\s+inet\s+dhcp.*?)(?=(?:iface\s|\Z)"

        match = re.search(pattern, content, re.DOTALL)

        if not match:
            print("Block not found")

        eth_block = match.group(1)

        new_eth_block = re.sub(r"(^\s*address\s+)(\d+\.\d+\.\d+\.\d+)", rf"\g<1>{self.ip_4}", eth_block, flags=re.MULTILINE, count=1)
        
        new_content = content.replace(eth_block, new_eth_block)

        with open("/tmp/interfaces", "w") as f:
            f.write(new_content)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        # subprocess.run(['sudo', 'tee', "/etc/network/interfaces"], input=new_config, text=True)

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
        # lines = []
        # changeable = False
        # with open("/etc/network/interfaces", "r") as f:
        #     for line in f:
        #         if line.strip().startswith(f"iface {self.name.lower()} inet"):
        #             lines.append(f"iface {self.name.lower()} inet dhcp\n")
        #             changeable = True
        #         elif not line.strip().startswith(("address", "netmask", "gateway", "hwaddress", "dns-nameservers")) and changeable == False:
        #             lines.append(line)


        with open("/etc/network/interfaces", "r") as f:
            content = f.read()

        def update_block(match: re.Match) -> str:
            header = match.group(1)
            body = match.group(1)
            header = f"iface {self.name.lower()} inet dhcp"
            body = re.sub(r"\n\s*(address|netmask|gateway|hwaddress|dns-nameservers)\s\S+", "", body)
            return header + body

        pattern = rf"(iface\s+{self.name.lower()}\s+inet\s+(?:static|dhcp))([\s\S]*?)(?=\niface|\Z)"

        new_content, count = re.subn(pattern, update_block, content, count=1, flags=re.MULTILINE)
        if count == 1:
            raise Exception(f"BLOCK NOT FOUND")

        with open("/tmp/interfaces", "w") as f:
            f.write(new_content)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)

        try:
            subprocess.run(['sudo', 'ifdown', self.name.lower()], check=True)
        except Exception:
            print("error")
        try:
            subprocess.run(['sudo', 'ifup', self.name.lower()], check=True)
        except Exception:
            print("error2")

        # with open("/tmp/interfaces", "w") as f:
        #     f.writelines(lines)
        #
        # # old file copy
        # with open("tmp/interfaces2", "w") as f:
        #     f.writelines(lines)

        # subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)


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
            #TODO: setting dynamic ip

            self.ip_4 = ip_address_field.value
            self.ip_4_field.value = self.ip_4
            self.mac_address = mac_address.value
            self.mac_address_field.value = self.mac_address
            self.mask = mask_field.value

            if dropdown4.value == "Вручную":
                self.set_static_ip4()
            elif dropdown4.value == "Использовать DHCP":
                self.set_dynamic_ip4()

            self.page.close(dialog)
            self.page.update()

        def handle_button_cancel(e):
            #TODO ↓ ♥
            if self.dynamic:
                dropdown4.value = "Использовать DHCP"
            else:
                dropdown4.value = "Вручную"

            ip_address_field.value = self.ip_4
            ip_address_field.disabled = True
            mask_field.value = self.mask
            mask_field.disabled = True

            mac_address.value = self.mac_address
            dropdown6.value = "Использовать DHCP"
            self.page.update()

        def ipv6_changed(e):
            selected = e.control.value
            print(selected)

            if selected == "Вручную":
                container.content = (
                    flet.Column([
                        flet.Row([
                            flet.Column([
                                flet.Text(value="IP-адрес", color="black"),
                                flet.Text(value="Маска подсети", color="black")
                            ]),
                            flet.Column([
                                flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange,
                                               height=40,
                                               width=250, fill_color=white, text_size=14),
                                flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange,
                                               height=40,
                                               width=250, fill_color=white, text_size=14)
                            ])
                        ])
                    ])
                )

            elif container.content is not None:
                container.content.clean()
            self.page.update()

        def ipv4_changed(e):
            selected = e.control.value
            print(selected)

            if selected == "Вручную":
                ip_address_field.disabled = False
                ip_address_field.value = self.ip_4
                mask_field.disabled = False
                mask_field.value = "0.0.0.0"

            else:
                ip_address_field.disabled = True
                ip_address_field.value = self.ip_4
                mask_field.disabled = True
                mask_field.value = "255.255.255.0"
            self.page.update()

        dropdown4 = flet.Dropdown(
            # TODO get static or dhcp from etc file and set dropdown start value
            value="Использовать DHCP" if self.get_static_or_dynamic() == "dhcp" else "Вручную",
            width=240,
            options=[
                flet.dropdown.Option("Использовать DHCP"),
                flet.dropdown.Option("Использовать BOOTP"),
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

        dropdown6 = flet.Dropdown(
            value="Использовать DHCP",
            width=240,
            options=[
                flet.dropdown.Option("Использовать DHCP"),
                flet.dropdown.Option("Использовать BOOTP"),
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

        # def ipv6_changed(e):
        #     selected = e.control.value
        #     print(selected)
        #
        #     if selected == "Вручную":
        #         container.content = (
        #             flet.Column([
        #                 flet.Row([
        #                     flet.Column([
        #                         flet.Text(value="IP-адрес", color="black"),
        #                         flet.Text(value="Маска подсети", color="black")
        #                     ]),
        #                     flet.Column([
        #                         flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
        #                             cursor_color=orange,
        #                                        height=40,
        #                                        width=250, fill_color=white, text_size=14),
        #                         flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
        #                             cursor_color=orange,
        #                                        height=40,
        #                                        width=250, fill_color=white, text_size=14)
        #                     ])
        #                 ])
        #             ])
        #         )
        #
        #     elif container.content is not None:
        #         container.content.clean()
        #     self.page.update()
        #
        # def ipv4_changed(e):
        #     selected = e.control.value
        #     print(selected)
        #
        #     if selected == "Вручную":
        #         ip_address_field.disabled = False
        #         ip_address_field.value = self.ip_4
        #         mask_field.disabled = False
        #         mask_field.value = "0.0.0.0"
        #
        #     else:
        #         ip_address_field.disabled = True
        #         ip_address_field.value = self.ip_4
        #         mask_field.disabled = True
        #         mask_field.value = "255.255.255.0"
        #     self.page.update()

        container = flet.Container()
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

        mac_address = flet.TextField(value=self.mac_address, bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
                                    cursor_color=orange, height=40, width=250, fill_color=white, text_size=14)
        button_cancel = flet.ElevatedButton(text="Отменить изменения", color=orange, bgcolor="white", width=209,
                                            height=28, on_click=handle_button_cancel, )
        button_save = flet.ElevatedButton(text="Применить", color="black", bgcolor=orange, width=137, height=28,
                                          on_click=handle_button_save, disabled = False)

        # dropdown4 = flet.Dropdown(
        #                 #TODO get static or dhcp from etc file and set dropdown start value
        #                 value = "Использовать DHCP" if self.get_static_or_dynamic() == "dhcp" else "Вручную",
        #                 width=240,
        #                 options=[
        #                     flet.dropdown.Option("Использовать DHCP"),
        #                     flet.dropdown.Option("Использовать BOOTP"),
        #                     flet.dropdown.Option("Вручную")
        #                 ],
        #                 border_radius=10,
        #                 color="black",
        #                 text_size=14,
        #                 bgcolor=orange,
        #                 border_color="black",
        #                 focused_border_color=orange,
        #                 on_change=ipv4_changed,
        # )
        #
        # dropdown6 = flet.Dropdown(
        #                 value="Использовать DHCP",
        #                 width=240,
        #                 options=[
        #                     flet.dropdown.Option("Использовать DHCP"),
        #                     flet.dropdown.Option("Использовать BOOTP"),
        #                     flet.dropdown.Option("Вручную"),
        #                 ],
        #                 border_radius=10,
        #                 color="black",
        #                 text_size=14,
        #                 bgcolor=orange,
        #                 border_color="black",
        #                 focused_border_color=orange,
        #                 on_change=ipv6_changed
        # )

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
                            flet.Text(value= "mac адрес", color= "black"),
                            mac_address
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


