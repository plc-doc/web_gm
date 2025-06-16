import flet
import os

from app_layout import AppLayout

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

DEFAULT_FLET_PORT = 1000
# flet_path = 'app'
flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))

class AuthorizationPage:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.title = "Authorization"
        self.page.vertical_alignment = flet.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        self.page.bgcolor = white
        # self.page.scroll = flet.ScrollMode.ADAPTIVE
        # self.store: DataStore = store

        self.user_name = ""
        self.password = ""




        self.tb = flet.TextField(bgcolor=white, label="Имя пользователя:", width=350, color="black", selection_color=orange,
                                 focused_border_color=orange, cursor_color=orange, border_radius=14)
        self.tb_password = flet.TextField(width=350, bgcolor=white, label="Пароль:", shift_enter=True, password=True,
                                          can_reveal_password=True, color="black", focused_border_color=orange,
                                          cursor_color=orange, selection_color=orange, border_radius=14)
        self.b = flet.ElevatedButton(text="Войти", on_click=self.button_clicked, bgcolor=orange, color="black", width=130,
                                     height=35)

        self.page.add(flet.Column(
                [
                            flet.Text(value="Авторизация",
                                      size=25,
                                      # font_family="Times New Roman",
                                      color= "black"),
                            flet.Column(controls=[self.tb, self.tb_password, self.b],
                                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                        spacing= 15,
                                        alignment=flet.MainAxisAlignment.CENTER)
                        ],
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        alignment=flet.MainAxisAlignment.CENTER,
                        spacing= 40))
        self.page.update()

    def button_clicked(self, e):
        # t.value = tb.value
        # t.update()
        # flet.Column(controls=[tb, t])
        if not self.tb.value:
            self.tb.error_text = "Please enter your name"
            self.page.update()
        elif not self.tb_password.value:
            self.tb_password.error_text = "Please enter password"
            self.page.update()
        #TODO: no user has entered user_name or password
        else:
            self.user_name = self.tb.value
            self.password = self.tb_password.value
            print(self.user_name, self.password)
            self.tb.update()
            self.tb_password.update()

            # self.page.clean()

            win = App(self.page)

            # self.page.clean()
            # self.page.add(win)


class App(AppLayout):
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.on_route_change = self.route_change

        self.appbar_items = [  # menu
            # self.login_profile_button,
            flet.PopupMenuItem(),  # divider
            flet.PopupMenuItem(text="Settings"),
        ]
        self.appbar = flet.AppBar(
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
        # self.page.add()

    def initialize(self):
        self.page.views.append(
            flet.View(
                "/",
                [self.appbar, self],
                padding=flet.padding.all(0),
                bgcolor=white,
            )
        )
        self.page.update()
        self.page.go("/")

    def route_change(self, e):
        troute = flet.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/settings")
        elif troute.match("/settings"):
            self.set_net_settings_view()
        elif troute.match("/clock"):
            self.set_clock_view()
        elif troute.match("/account"):
            print("account")
        self.page.update()


flet.app(target=AuthorizationPage, view=flet.WEB_BROWSER,host= "192.168.1.58",port=flet_port, assets_dir="assets")
