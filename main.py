import asyncio
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from multiprocessing.reduction import duplicate

import flet
import os
import hashlib

import User
from app_layout import AppLayout

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

DEFAULT_FLET_PORT = 80
# flet_path = 'app'
flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))

'''
  Authorization
  Switches to App
'''
class AuthorizationPage:
    def __init__(self, page: flet.Page):
        self.page = page
        # self.page.favicon = "favicon.png"
        self.page.title = "GMB"
        self.page.vertical_alignment = flet.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        self.page.bgcolor = white
        # self.page.scroll = flet.ScrollMode.ADAPTIVE
        # self.store: DataStore = store

        self.user_name = ""
        self.password = ""

        self.tb = flet.TextField(bgcolor=white, label="Имя пользователя:", width=350, color="black", selection_color=orange,
                                 focused_border_color=orange, cursor_color=orange, border_radius=14, on_click=self.on_click)
        self.tb_password = flet.TextField(width=350, bgcolor=white, label="Пароль:", shift_enter=True, password=True,
                                          can_reveal_password=True, color="black", focused_border_color=orange,
                                          cursor_color=orange, selection_color=orange, border_radius=14, on_click= self.on_click)
        self.b = flet.ElevatedButton(text="Войти", on_click=self.button_clicked, bgcolor=orange, color="black", width=130,
                                     height=35)

        self.error_text = flet.Text(value="Не удалось войти. Неверный логин или пароль", color="red", size=15, visible=False)

        self.page.add(flet.Column(
                    [
                            flet.Text(value="Авторизация",
                                      size=25,
                                      color= "black"),
                            flet.Column(controls=[self.error_text ,
                                                  self.tb,
                                                  self.tb_password,
                                                  self.b,
                                                  ],
                                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                        spacing= 15,
                                        alignment=flet.MainAxisAlignment.CENTER)
                            ],
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                            alignment=flet.MainAxisAlignment.CENTER,
                            spacing= 40
        ))
        self.page.update()

        self.column = flet.Column(
                    [
                            flet.Text(value="Авторизация",
                                      size=25,
                                      color= "black"),
                            flet.Column(controls=[self.error_text ,
                                                  self.tb,
                                                  self.tb_password,
                                                  self.b,
                                                  ],
                                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                        spacing= 15,
                                        alignment=flet.MainAxisAlignment.CENTER)
                            ],
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                            alignment=flet.MainAxisAlignment.CENTER,
                            spacing= 40
        )

        self.initialize()

    #routing "/" for button logout
    def initialize(self):
        self.page.views.append(
            flet.View(
                "/",
                [self.column],
                padding=flet.padding.all(0),
                bgcolor=white,
                vertical_alignment=flet.MainAxisAlignment.CENTER,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()
        self.page.go("/")

    # hide error texts
    def on_click(self, e):
        print('a')
        self.error_text.visible = False
        self.tb.error_text = None
        self.tb_password.error_text = None
        self.page.update()

    def button_clicked(self, e):
        if not self.tb.value:
            self.tb.error_text = "Пожалуйста, введите логин"
            self.page.update()
        elif not self.tb_password.value:
            self.tb_password.error_text = "Пожалуйста, введите пароль"
            self.page.update()
        else:
            if User.get_user(self.tb.value, hashlib.sha256(self.tb_password.value.encode()).hexdigest()):
                self.user_name = self.tb.value
                self.password = self.tb_password.value
                print(self.user_name, self.password)
                self.tb.update()
                self.tb_password.update()

                win = App(self.page)
            else:
                self.tb_password.error_text = ""
                self.error_text.visible = True

                self.page.update()


class App(AppLayout):
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.DEFAULT_FLET_PORT = DEFAULT_FLET_PORT
        self.ip_dict = {} #{fd : "ip"}
        self.used_ip_dict = {}
        self.user_ip = self.get_user_ip()

        self.appbar_items = [  # menu
            # self.login_profile_button,
            flet.PopupMenuItem(),  # divider
            flet.PopupMenuItem(text="Settings"),
        ]

        self.appbar = flet.AppBar( # invisible appbar, without which doesn't work
            leading=flet.Icon(flet.Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=flet.Text(
                f"Trolli",
                font_family="Pacifico",
                size=32,
                text_align=flet.TextAlign.START,
            ),
            center_title=False,
            toolbar_height=75,
            bgcolor=flet.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                flet.Container(
                    content=flet.PopupMenuButton(items=self.appbar_items),
                    margin=flet.margin.only(left=50, right=25),
                )
            ],
            visible=False,
        )
        self.page.appbar = self.appbar
        self.page.update()

        super().__init__(  # calling AppLayout class
            self,
            self.page,
            # self.store,
            tight=True,
            expand=True,
            vertical_alignment=flet.CrossAxisAlignment.START,
        )

        self.initialize()

    def initialize(self):
        self.page.views.append(
            flet.View(
                "/start",
                [self.appbar, self],
                padding=flet.padding.all(0),
                bgcolor=white,
            )
        )
        self.page.update()
        self.page.go("/start")

    def route_change(self, e):
        troute = flet.TemplateRoute(self.page.route)
        if troute.match("/start"):
            self.page.go("/settings")
        elif troute.match("/settings"):
            self.set_net_settings_view()
        elif troute.match("/clock"):
            self.set_clock_view()
        elif troute.match("/info"):
            self.set_info_view()
        elif troute.match("/"):
            AuthorizationPage(self.page)

        self.page.update()

    # def get_user_ip(self):
    #     cmd = f"sudo ss -tnp | grep {DEFAULT_FLET_PORT}"
    #     result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    #
    #     lines = result.stdout.strip().splitlines()
    #     if not lines:
    #         return " - "
    #
    #     first_line = lines[0]
    #
    #
    #     match = re.search(r'\s+\d+\.\d+\.\d+\.\d+:\d+\s+(\d+\.\d+\.\d+\.\d+):\d+', first_line)
    #     if match:
    #         ip = match.group(1)
    #         return ip
    #     else:
    #         return " x "

    def get_user_ip(self):
        cmd = f"sudo ss -tnp | grep {DEFAULT_FLET_PORT}"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        lines = result.stdout.strip().splitlines()
        groups = defaultdict(list)

        for line in lines:
            match = re.search(r'\s+\d+\.\d+\.\d+\.\d+:\d+\s+(\d+\.\d+\.\d+\.\d+):\d+', line)
            m = re.search(r'fd=(\d+)', line)
            if match:
                ip = match.group(1)
                if m:
                    fd = int(m.group(1))
                    # for key, value in ip_dict.items():
                    # if key == fd and value == ip:
                    #     continue
                    # else:
                    #     del ip_dict[key]
                    for key, value in list(self.ip_dict.items()):
                        if fd in self.ip_dict:
                            if value != ip:
                                del self.ip_dict[fd]

                    # Группируем ключи по значениям, пропуская ключи из self.used_ip_dict
                    # for key, value in self.ip_dict.items():
                    if fd not in self.ip_dict:  # <-- пропускаем
                        groups[ip].append(fd)
                        self.ip_dict[fd] = ip

                else:
                    return "False"
            else:
                return " - "
            # Берём максимальные ключи для каждого значения
        max_v = {value: max(keys) for value, keys in groups.items()}
        self.used_ip_dict.update(max_v)

        return next(iter(max_v))

flet.app(target=AuthorizationPage, view=flet.WEB_BROWSER, host= "0.0.0.0", port=flet_port, assets_dir="assets")
