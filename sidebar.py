import flet

import User

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class Sidebar(flet.Container):

    def __init__(self, app_layout):
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            flet.NavigationRailDestination(
                icon=flet.Icons.CAST_CONNECTED,
                selected_icon=flet.Icons.CAST_CONNECTED,
                label_content=flet.Text(value="Настройка сети", color="black"),
                padding =flet.padding.all(0)
            ),
            flet.NavigationRailDestination(
                icon=flet.Icon(flet.Icons.ACCESS_TIME_FILLED),
                selected_icon=flet.Icons.ACCESS_TIME_FILLED,
                # label="Системное время",
                label_content=flet.Text(value="Системное время", color="black"),
                padding=flet.padding.all(0)
            ),
        ]

        self.rail = flet.NavigationRail(
            selected_index=0,
            label_type=flet.NavigationRailLabelType.ALL,
            min_width=140,
            min_extended_width=400,
            bgcolor=white,  # navigation rail bg color
            indicator_color=orange,
            expand=True,
            leading=flet.FloatingActionButton(
                text="Add",
                content=flet.SubmenuButton(
                    content=flet.CircleAvatar(
                        foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
                        bgcolor="white",  # avatar inner circle color
                        color="black",  # avatar text color
                        content=flet.Text("AB"),
                    ),
                    controls=[
                        flet.Container(
                            content=flet.CupertinoButton(
                                "Профиль",
                                opacity_on_click=0.3,
                                on_click=self.handle_profile_button,
                                color="black",
                                icon=flet.Icons.ACCOUNT_CIRCLE,
                                icon_color="black"
                            ),
                            bgcolor="#CACACA",
                            padding=0,
                            width=140,
                        ),
                        flet.Container(
                            content=flet.ElevatedButton("Выйти", on_click=lambda e: self.app_layout.route_change(e), bgcolor="red",
                                                        color=white, width=10),
                            bgcolor="#CACACA",
                            padding=0,
                            width=140,
                        ),
                    ],
                    height=30
                ),
                on_click=self.nav_change,
                bgcolor=orange,
            ),
            group_alignment=-0.9,
            destinations=self.top_nav_items,
            on_change=self.nav_change,
        )

        super().__init__(
            content=flet.Column(controls=[self.rail]),
            padding=flet.padding.all(15),
            margin=flet.margin.all(0),
            width=140,
            bgcolor=white,
            visible=self.nav_rail_visible,
        )

    def handle_profile_button(self, x):
        def change_password(e):
            login = dialog_field.controls[0].value
            new_password = dialog_field.controls[1].value
            repeat_password = dialog_field.controls[2].value

            if User.get_user_login(login):  # if login is correct(user exists)
                if new_password == repeat_password:
                    User.change_password(login, new_password)
                    print("successfully change password")
                else:
                    dialog_field.controls[1].value = ""
                    dialog_field.controls[2].value = ""
                    dialog_field.controls[1].error_text = "Пароли не совпадают"
                    dialog_field.controls[2].error_text = "Пароли не совпадают"
                    self.page.update()
                    return
            else:
                dialog_field.controls[0].error_text = "Пользователя с таким логином не существует"
                dialog_field.controls[1].value = ""
                dialog_field.controls[2].value = ""
                self.page.update()
                return

            self.page.close(dialog)
            self.page.update()

        def on_click(e):
            print('a')
            dialog_field.controls[0].error_text = None
            dialog_field.controls[1].error_text = None
            dialog_field.controls[2].error_text = None
            self.page.update()

        dialog_field = (
            flet.Column(
                [flet.TextField(bgcolor=white, label="Имя пользователя:", width=350, color="black",
                                selection_color=orange, on_click = on_click,
                                focused_border_color="orange", cursor_color="orange", border_radius=14),
                 flet.TextField(bgcolor=white, label="Новый пароль:", width=350, color="black",
                                selection_color=orange, on_click = on_click,
                                focused_border_color=orange, cursor_color=orange, border_radius=14),
                 flet.TextField(bgcolor=white, label="Повторите пароль:", width=350, color="black",
                                selection_color=orange,on_click = on_click,
                                focused_border_color=orange, cursor_color=orange, border_radius=14),
                 flet.ElevatedButton(text="Сохранить", color="black", bgcolor=orange, on_click=change_password)
                 ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                alignment=flet.MainAxisAlignment.CENTER,
                spacing=40

            ))

        dialog = flet.AlertDialog(
            content=flet.Container(
                width=400,
                height=350,
                content=dialog_field
            ),
            bgcolor="white",
            on_dismiss=lambda e: print("Dialog dismissed!"),
            content_padding=50,
        )

        self.page.open(dialog)
        dialog.open = True
        self.page.update()

    def nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.rail.selected_index = index
        print(f"index = {index}")
        if index == 0:
            self.page.route = "/settings"
        elif index == 1:
            self.page.route = "/clock"
        self.page.update()