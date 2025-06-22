import asyncio
import re

import flet
import datetime
import subprocess
from flask import Flask, request

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

# now = datetime.datetime.now()

# time = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"

class ClockView:
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.date_field = flet.Text(value= self.get_date(), color= "black")
        self.time_field = flet.Text( color="black")

        self.NTP_servers = []
        self.NTP = False
        self.start_NTP = self.NTP
        self.servers_count = 0

        self.servers_column = flet.Column()

        self.time_zone = flet.Dropdown(
                                value= self.get_time_zone().strip(),
                                width=240,
                                menu_height = 400,
                                options=self.get_time_zones_list(),
                                border_radius=10,
                                color="black",
                                text_size=14,
                                bgcolor=grey,
                                border_color="black",
                                focused_border_color=white,
                                filled =True,
                                fill_color=white
                                # on_change=ipv6_changed
                            )

        # self.ntp_servers = flet.Dropdown()
        # self.option_textbox = flet.TextField(hint_text="Enter item name")
        # self.add = flet.ElevatedButton("Добавить NTP сервер", on_click=self.add_clicked)

        # self.get_time()

        # super().__init__(
        #     flet.Column(
        #     controls=[
        #         flet.Text("Настройка даты и времени", text_align=flet.alignment.center,color=orange,size=20),
        #         flet.Container(
        #             padding= 20,
        #             bgcolor="#CACACA",
        #             width=1050,
        #             height=293,
        #             border_radius=30,
        #             alignment=flet.alignment.center,
        #             content=flet.Column([
        #                 flet.Text("Настройки локального времени", color= "black", size= 18),
        #                 flet.Row([
        #                     flet.Column([
        #                         flet.Text("Дата", color="black"),
        #                         flet.Text("Время", color="black")
        #                     ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30),
        #                     flet.Column([
        #                         self.date_field,
        #                         self.time_field
        #                     ], horizontal_alignment=flet.CrossAxisAlignment.CENTER),
        #                     flet.FilledTonalButton(text="Синхронизировать с компьютером",
        #                                           bgcolor=orange,
        #                                           color="black",
        #                                           on_click=lambda e: print()
        #                                            )
        #                 ], alignment=flet.MainAxisAlignment.SPACE_EVENLY),
        #                 flet.VerticalDivider(width= 946, color= "#ACACAC"),
        #                 flet.Row([
        #                     flet.Text("Часовой пояс", color="black"),
        #                     flet.TextField(value=self.get_time_zone(), border=flet.InputBorder.NONE, color="black")
        #
        #                 ], alignment=flet.MainAxisAlignment.CENTER, spacing= 30)
        #             ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
        #         ),
        #         flet.Container(bgcolor="#CACACA",
        #             padding= 20,
        #             width=1050,
        #             height=293,
        #             border_radius=30,
        #             alignment=flet.alignment.center,
        #             content=flet.Column([
        #                 flet.Text("Синхронизация времени", color="black", size=18),
        #                 flet.Row([
        #                     flet.Column([
        #                         flet.Text("Синхронизация времени при помощи NTP", color="black"),
        #                         flet.Text("NTP - серверы", color= "black")
        #                     ], horizontal_alignment=flet.CrossAxisAlignment.END, spacing= 30),
        #                     flet.Column([
        #                         flet.CupertinoSwitch(value= False, active_color=orange),
        #
        #                     ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30)
        #                 ], alignment=flet.MainAxisAlignment.SPACE_EVENLY)
        #             ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
        #         )
        #     ],
        #     horizontal_alignment=flet.CrossAxisAlignment.CENTER
        #     ),
        #     expand=True,
        #     padding=20
        # )
        self.button_save = flet.ElevatedButton(text="Сохранить изменения",
                                             bgcolor=orange,
                                             color="black",
                                             on_click= lambda e: self.handle_button_save()
                                             )
        self.button_cancel = flet.ElevatedButton(text="Отменить изменения",
                                                  bgcolor=white,
                                                  color=orange,
                                                  on_click= lambda e: self.handle_button_cancel()
                                                  )

        self.container = flet.Container(flet.Column(
            controls=[
                flet.Text("Настройка даты и времени", text_align=flet.alignment.center,color=orange,size=20),
                flet.Container(
                    padding= 20,
                    bgcolor="#CACACA",
                    width=1050,
                    height=293,
                    border_radius=30,
                    alignment=flet.alignment.center,
                    content=flet.Column([
                        flet.Text("Настройки локального времени", color= "black", size= 18),
                        flet.Row([
                            flet.Column([
                                flet.Text("Дата", color="black"),
                                flet.Text("Время", color="black")
                            ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30),
                            flet.Column([
                                self.date_field,
                                self.time_field
                            ], horizontal_alignment=flet.CrossAxisAlignment.CENTER),
                            # self.button
                        ], alignment=flet.MainAxisAlignment.SPACE_EVENLY),
                        flet.VerticalDivider(width= 946, color= "#ACACAC"),
                        flet.Row([
                            flet.Text("Часовой пояс", color="black"),
                            self.time_zone
                        ], alignment=flet.MainAxisAlignment.CENTER, spacing= 30)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
                ),
                flet.Container(bgcolor="#CACACA",
                    padding= 20,
                    width=1050,
                    height=400,
                    border_radius=30,
                    alignment=flet.alignment.center,
                    content=flet.Column([
                        flet.Text("Синхронизация времени", color="black", size=18),
                        flet.Row([
                            flet.Column([
                                flet.Text("Синхронизация времени при помощи NTP", color="black"),
                                flet.Row([
                                    flet.Text("NTP - серверы", color= "black")

                                ]),
                            ], horizontal_alignment=flet.CrossAxisAlignment.END, spacing= 30),
                            flet.Column([
                                flet.CupertinoSwitch(value= self.NTP_on_or_off(),disabled= True if self.NTP else False,active_color=orange, on_change=self.switch),
                                # flet.Column(controls=[self.ntp_servers, flet.Row(controls=[self.option_textbox, self.add])])
                                self.NTC_servers(),
                            ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30)
                        ], alignment=flet.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=flet.CrossAxisAlignment.START)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
                ),
                flet.Row([
                    self.button_cancel,
                    self.button_save
                ], alignment=flet.MainAxisAlignment.CENTER, vertical_alignment=flet.CrossAxisAlignment.CENTER, spacing = 40)


            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER
            ),
            expand=True,
            padding=20
        )
        self.page.update()

        self.get_time()
        # self.button_save.on_click = lambda e: self.stop_time()
        # self.time_field.on_click = lambda e: self.time_changed()
        # self.date_field.on_click = lambda e: self.date_changes()

    # def add_clicked(self, e):
    #     self.ntp_servers.options.append(flet.dropdown.Option(self.option_textbox.value))
    #     self.ntp_servers.value = self.option_textbox.value
    #     self.option_textbox.value = ""
    #     self.option_textbox.update()
    #     self.ntp_servers.update()

    def NTP_on_or_off(self):
        r = subprocess.run(["timedatectl", "status"], capture_output=True, check=True, text=True)
        result = r.stdout.split("\n")

        for line in result:
            if line.startswith("NTP service"):
                if line.split(":", 1)[1] == "active":
                    self.NTP = True

        return self.NTP


    def switch(self, e):
        turn_on = e.control.value
        self.NTP = turn_on

        print(turn_on)

    def handle_button_save(self):
        global task

        # if task.cancelled():
        # self.set_local_datetime()

        # if self.time_zone.value != self.get_time_zone():
        if self.start_NTP != self.NTP:
            if self.NTP:
                self.turn_on_NTP()
            else:
                self.turn_off_NTP()

        self.set_time_zone()

        self.set_NTP_servers()
        # self.date_field.value = self.get_date()
        self.time_zone.value = self.get_time_zone()
        # self.stop_time()
        self.get_time()
        self.get_date()
        # self.time_field.filled = False
        # self.date_field.filled = False
        # self.time_field.border = flet.InputBorder.NONE
        # self.date_field.border = flet.InputBorder.NONE

        self.page.update()

    def handle_button_cancel(self):
        self.stop_time()
        self.date_field.value = self.get_date()
        self.get_time()
        # self.time_field.filled = False
        # self.date_field.filled = False
        # self.time_field.border= flet.InputBorder.NONE
        # self.date_field.border= flet.InputBorder.NONE

        self.page.update()

    def NTC_servers(self):
        # servers_column = flet.Column()

        with open("/etc/systemd/timesyncd.conf", "r") as f:
            for line in f:
                if line.startswith("NTP"):
                    servers = re.findall(r'[\w.\-]+', line.split("=", 1)[1])


        for server in servers:
            print(server)
            s = flet.TextField(filled=True, fill_color=white, color="black")
            s.value = server
            self.NTP_servers.append(s)

            self.servers_column.controls.append(flet.Row(
                                                    [s,
                                                     flet.IconButton(
                                                        icon=flet.Icons.DELETE_FOREVER_ROUNDED,
                                                        icon_color="red",
                                                        icon_size=23,
                                                        on_click = lambda e: self.delete_server)
                                                     ]
            ))

            self.servers_count += 1

        self.servers_column.controls.append(flet.Row([flet.TextField(filled=True, fill_color=white, color="black"),
                                                     flet.IconButton(
                                                        icon=flet.Icons.ADD_BOX,
                                                        icon_color="green",
                                                        icon_size=20,
                                                        on_click = self.add_server
                                                    )
                                        ]))

        return self.servers_column

    def delete_server(self, e):
        for i, controls in enumerate(self.servers_column.controls):
            if e.control == controls.controls[1]:
                self.servers_column.controls.pop(i)

        # self.servers_column.controls.pop()
        self.page.update()

    def add_server(self, e):
        self.servers_column.controls.insert(len(self.servers_column.controls) - 1,
                                            flet.Row([flet.TextField(filled=True, fill_color=white, color="black"),
                                                      flet.IconButton(
                                                          icon=flet.Icons.DELETE_FOREVER_ROUNDED,
                                                          icon_color="red",
                                                          icon_size=23,
                                                          on_click=self.delete_server)
                                                      ]))
        self.page.update()


    def set_NTP_servers(self):
        lines = []

        with open("/etc/systemd/timesyncd.conf", "r") as f:
            for line in f:
                if line.startswith("NTP"):
                    string = f"NTP= "
                    for s in self.NTP_servers:
                        string += f"{s.value }"
                    print(string)
                    string += "\n"
                    lines.append(string)
                else:
                    lines.append(line)

        with open("/tmp/interfaces", "w") as f:
            f.writelines(lines)

        # old file copy
        with open("/tmp/interfaces2", "w") as f:
            f.writelines(lines)

        subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"], check=True)


    # def time_changed(self):
    #     global task
    #
    #     self.stop_time()
    #     self.time_field.filled = True
    #     self.time_field.bgcolor = white
    #     self.time_field.border = flet.InputBorder.OUTLINE
    #     self.time_field.border_radius = 14
    #     self.time_field.focused_border_color = orange
    #
    #     self.page.update()
    #
    # def date_changes(self):
    #     self.date_field.filled = True
    #     self.date_field.bgcolor = white
    #     self.date_field.border = flet.InputBorder.OUTLINE
    #     self.date_field.border_radius = 14
    #     self.date_field.focused_border_color = orange
    #
    #     self.page.update()

    def stop_time(self):
        global task

        task.cancel()
        self.page.update()

    def get_date(self):
        # date = datetime.date.today().strftime("%d.%m.%Y")
        # date = 3

        r = subprocess.run(["timedatectl", "status"], capture_output=True, check=True, text=True)
        now = r.stdout.split()[3]
        #
        # date = self.date_field.value
        date_obj = datetime.datetime.strptime(now, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")

        # r = subprocess.run("")
        # now = datetime.datetime.now()
        # formatted_date = f"{now.day:02d}.{now.month:02d}.{now.year}"

        # self.get_time()

        return str(formatted_date)

    def get_time(self):
        global task
        async def update_time():
            # global time
            while True:
                r = subprocess.run(["timedatectl", "status"], capture_output=True, check=True, text=True)
                now = r.stdout.split()[4]
                # now = datetime.datetime.now()

                # self.time_field.value = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
                self.time_field.value = now
                self.page.update()
                await asyncio.sleep(1)

        task = self.page.run_task(update_time)


    # def set_local_datetime(self):
    #     date = self.date_field.value
    #     date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    #     formatted_date = date_obj.strftime("%Y-%m-%d")
    #     subprocess.run(["sudo", "date", "--set", f"{formatted_date} {self.time_field.value}"])
    #
    #     self.page.update()

    def set_time_zone(self):
        subprocess.run(["sudo", "timedatectl", "set-timezone", self.time_zone.value],check=True)

        # lines = []
        # with open("/etc/timezone", "r") as f:
        #     for line in f:
        #         lines.append(self.time_zone.value)
        #
        # with open("/tmp/timezone", "w") as f:
        #     f.writelines(self.time_zone.value)
        #
        # # with open("/etc/timezone", "w") as f:
        # #     f.writelines(lines)
        #
        # subprocess.run(["sudo", "cp", "/tmp/timezone", "/etc/timezone"], check=True)
        #
        # subprocess.run(["sudo", "systemctl", "restart", "systemd-timesyncd.service"], check=True)

    def get_time_zone(self):
        # time_zone = subprocess.run(["cat", '/etc/timezone'], capture_output=True, text=True, check= True)
        # result = time_zone.stdout
        # print(result)
        # return result

        request_timezone = subprocess.run(['timedatectl', 'status'], text = True, capture_output=True, check=True)
        result = request_timezone.stdout

        for line in result.strip().split('\n'):

            if line.startswith("                Time zone:"):
                timezone = line.split(":", 1)[1].split("(",1)[0].strip()
                return timezone

        return "None"

    def get_time_zones_list(self):
        result = subprocess.run(["timedatectl","list-timezones"], capture_output=True, check=True, text=True)
        time_zones = result.stdout.strip().split('\n')

        options = []

        for time_zone in time_zones:
            options.append(flet.dropdown.Option(time_zone))

        return options

    def turn_on_NTP(self):
        subprocess.run(["sudo", "timedatectl", "set-ntp", "true"], check = True)

    def turn_off_NTP(self):
        subprocess.run(["sudo", "timedatectl", "set-ntp", "false"], check = True)
        subprocess.run(["sudo", "systemctl", "reboot"])


    # TODO:
    #  setting NTP and choosing servers (list)

    # def set_time(self):
    # def set_date(self):
    # def set_ntp_server(self):
