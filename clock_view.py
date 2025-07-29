import asyncio
import re

import flet
import datetime
import subprocess

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class ClockView:
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.date_field = flet.Text(value= self.get_date(), color= "black")
        self.time_field = flet.Text( color="black")

        self.NTP_servers = []
        self.NTP = False # Ntp active or not
        self.start_NTP = self.NTP_on_or_off() #start value of ntp
        self.servers_count = 0

        self.page.on_resized = self.resize

        self.servers_column = flet.Column(height=250, scroll=flet.ScrollMode.AUTO)

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

        # banner with reboot warning
        # TODO: give it functionality (buttons restart and cancel)
        self.banner = flet.Banner(
            bgcolor=flet.Colors.AMBER_100,
            leading=flet.Icon(flet.Icons.WARNING_AMBER_ROUNDED, color="black", size=40),
            content=flet.Text("Restart", color="black"),
            actions=[
                flet.TextButton("Отменить", on_click=self.close_banner),
                flet.TextButton("Перезагрузить", on_click=self.close_banner),
            ],
            content_padding= flet.padding.only(left=316.0, top=24.0, right=16.0, bottom=4.0)
        )

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

        # Clock view layout
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
                flet.Container(
                    bgcolor="#CACACA",
                    padding= 20,
                    width=1050,
                    height=400,

                    # height=self.app.page.height,
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
                                flet.CupertinoSwitch(value= self.NTP_on_or_off(),active_color=orange, on_change=self.switch),
                                # flet.Column(controls=[self.ntp_servers, flet.Row(controls=[self.option_textbox, self.add])])
                                self.NTC_servers(),
                            ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30, scroll=flet.ScrollMode.AUTO)
                        ], alignment=flet.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=flet.CrossAxisAlignment.START)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
                ),
                flet.Row([
                    self.button_cancel,
                    self.button_save
                ], alignment=flet.MainAxisAlignment.CENTER, vertical_alignment=flet.CrossAxisAlignment.CENTER, spacing = 40)
            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER, scroll=flet.ScrollMode.AUTO,
            ),
            expand=True,
            padding=20
        )
        self.page.update()

        self.get_time()

    def NTP_on_or_off(self):
        try:
            r = subprocess.run(["timedatectl", "status"], capture_output=True, check=True, text=True)
            result = r.stdout.strip().split("\n")

            for line in result:
                if line.startswith("              NTP service"):
                    print(line)
                    if line.split(":", 1)[1].strip() == "active":
                        print(line.split(":", 1)[1])
                        self.NTP = True

            return self.NTP
        except Exception:
            return ""

    def switch(self, e):
        turn_on = e.control.value
        self.NTP = turn_on

        print(turn_on)

    # adding scrollbar if ntp servers count > 3
    def resize(self):
        self.servers_column.height += 50
        # self.NTP_container.width = width
        print(self.servers_column.height)
        self.page.update()

    def handle_button_save(self):
        global task

        self.show_banner_click()

        if self.start_NTP != self.NTP:
            if self.NTP:
                print('on')
                self.turn_on_NTP()
            else:
                self.set_time_zone()
                self.set_NTP_servers()
                print('off')
                self.show_banner_click()
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
        try:
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
                                                            on_click = self.delete_server)
                                                         ], scroll = flet.ScrollMode.AUTO
                ))

                self.servers_count += 1

            self.servers_column.controls.append(flet.Row(
                                            [
                                                     flet.TextField(filled=True, fill_color=white, color="black"),
                                                     flet.IconButton(
                                                        icon=flet.Icons.ADD_BOX,
                                                        icon_color="green",
                                                        icon_size=20,
                                                        on_click = self.add_server
                                                    )
                                                    ],scroll = flet.ScrollMode.AUTO)
            )

            return self.servers_column
        except Exception:
            return self.servers_column

    def delete_server(self, e):
        for i, controls in enumerate(self.servers_column.controls):
            if e.control == controls.controls[1]:
                self.servers_column.controls.pop(i)
                self.NTP_servers.pop(i)
                print(i)
        self.servers_count -= 1

        # self.servers_column.controls.pop()
        # if self.servers_count <= 3:
        #     self.servers_column.height = 200
        self.page.update()

    def add_server(self, e):
        s = flet.TextField(filled=True, fill_color=white, color="black")
        self.servers_column.controls.insert(len(self.servers_column.controls) - 1,
                                            flet.Row([s,
                                                      flet.IconButton(
                                                          icon=flet.Icons.DELETE_FOREVER_ROUNDED,
                                                          icon_color="red",
                                                          icon_size=23,
                                                          on_click=self.delete_server)
                                                      ]))

        self.NTP_servers.append(s)
        self.servers_count += 1

        # if self.servers_count > 3:
        #     self.resize()
        self.page.update()


    def set_NTP_servers(self):
        lines = []

        try:
            with open("/etc/systemd/timesyncd.conf", "r") as f:
                for line in f:
                    if line.startswith("NTP"):
                        string = f"NTP= "
                        for s in self.NTP_servers:
                            string += f"{s.value} "
                        print(string)
                        string += "\n"
                        lines.append(string)
                    else:
                        lines.append(line)

            with open("/tmp/interfaces", "w") as f:
                f.writelines(lines)

            # old file copy

            subprocess.run(["sudo", "cp", "/tmp/interfaces", "/etc/systemd/timesyncd.conf"], check=True)
        except Exception:
            print("")

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

        try:
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
        except Exception:
            return ""

    def get_time(self):
        global task
        async def update_time():
            # global time
            try:
                while True:
                    r = subprocess.run(["timedatectl", "status"], capture_output=True, check=True, text=True)
                    now = r.stdout.split()[4]
                    # now = datetime.datetime.now()

                    # self.time_field.value = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
                    self.time_field.value = now
                    self.page.update()
                    await asyncio.sleep(1)
            except Exception:
                self.time_field.value = ""

        task = self.page.run_task(update_time)


    # def set_local_datetime(self):
    #     date = self.date_field.value
    #     date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    #     formatted_date = date_obj.strftime("%Y-%m-%d")
    #     subprocess.run(["sudo", "date", "--set", f"{formatted_date} {self.time_field.value}"])
    #
    #     self.page.update()

    def set_time_zone(self):
        try:
            subprocess.run(["sudo", "timedatectl", "set-timezone", self.time_zone.value],check=True)
        except Exception:
            print("")

    def get_time_zone(self):
        try:
            request_timezone = subprocess.run(['timedatectl', 'status'], text = True, capture_output=True, check=True)
            result = request_timezone.stdout

            for line in result.strip().split('\n'):

                if line.startswith("                Time zone:"):
                    timezone = line.split(":", 1)[1].split("(",1)[0].strip()
                    return timezone

            return "None"
        except Exception:
            return ""

    def get_time_zones_list(self):
        options = []

        try:
            result = subprocess.run(["timedatectl","list-timezones"], capture_output=True, check=True, text=True)
            time_zones = result.stdout.strip().split('\n')

            for time_zone in time_zones:
                options.append(flet.dropdown.Option(time_zone))

            return options
        except Exception:
            return options

    def turn_on_NTP(self):
        try:
            subprocess.run(["sudo", "timedatectl", "set-ntp", "true"], check = True)
        except Exception:
            print("")

    def turn_off_NTP(self):
        try:
            subprocess.run(["sudo", "timedatectl", "set-ntp", "false"], check = True)
            subprocess.run(["sudo", "systemctl", "reboot"])
        except Exception:
            print("")

    def close_banner(self, e):
        self.banner.open = False
        self.page.update()

    def show_banner_click(self):
        self.page.overlay.append(self.banner)
        self.banner.open = True
        self.page.update()

