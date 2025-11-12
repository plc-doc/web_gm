import flet

import User

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class Sidebar(flet.Container):

    def __init__(self, app_layout):
        # self.page = page
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.prev_nav = 0
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
            flet.NavigationRailDestination(
                icon=flet.Icon(flet.Icons.SETTINGS_BACKUP_RESTORE_ROUNDED,),
                selected_icon=flet.Icon(flet.Icons.SETTINGS_BACKUP_RESTORE_ROUNDED,),
                label_content=flet.Text(value="Сброс до заводских настроек", color="black", text_align=flet.TextAlign.CENTER),
                padding = flet.padding.all(0)
            ),
            flet.NavigationRailDestination(
                icon=flet.Icon(flet.Icons.UPLOAD_ROUNDED, ),
                selected_icon=flet.Icon(flet.Icons.UPLOAD_ROUNDED, ),
                label_content=flet.Text(value="Загрузка проекта CodeSys", color="black", text_align=flet.TextAlign.CENTER),
                padding=flet.padding.all(0)
            ),
            flet.NavigationRailDestination(
                icon=flet.Icon(flet.Icons.INFO_ROUNDED, ),
                selected_icon=flet.Icon(flet.Icons.INFO_ROUNDED, ),
                label_content=flet.Text(value="Состояние", color="black"),
                padding=flet.padding.all(0),
            ),
            flet.NavigationRailDestination(
                icon=flet.Icon(flet.Icons.DEVICE_HUB_ROUNDED, ),
                selected_icon=flet.Icon(flet.Icons.DEVICE_HUB_ROUNDED, ),
                label_content=flet.Text(value="Подключенные слейвы", color="black", text_align=flet.TextAlign.CENTER),
                padding=flet.padding.all(0),
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
                        # content=flet.Text("sa"),
                        content=flet.Image("favicon.png"),
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
                            content=flet.ElevatedButton("Выйти", on_click=lambda _: self.page.go("/"), bgcolor="red",
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
        # my_style = flet.TextStyle(size=12)
        # my_style = flet.TextStyle(size=12)
        self.error_text = flet.Text(value="Не удалось изменить пароль", color="red", size=15, visible=False)


        self.doc_button = flet.ElevatedButton(content=flet.Container(flet.Column([
                                                        flet.Icon(name=flet.Icons.FILE_OPEN_ROUNDED,
                                                                  color={flet.ControlState.DEFAULT:"orange",
                                                                         flet.ControlState.HOVERED:"black"}),
                                                        flet.Text(value="Документация\n", size=12)
                                                        ],horizontal_alignment=flet.CrossAxisAlignment.CENTER),padding=3),
                                              on_click=self.open_html_documentation,
                                              # style=flet.ButtonStyle(text_style=my_style),
                                              color={flet.ControlState.DEFAULT: "black",
                                                     flet.ControlState.HOVERED:"black"},
                                              bgcolor={flet.ControlState.DEFAULT: white,
                                                       flet.ControlState.HOVERED:orange},
                                              style=flet.ButtonStyle(shape=flet.ContinuousRectangleBorder(radius=50),
                                                                     side={flet.ControlState.DEFAULT: flet.BorderSide(2, "orange")},),
                                              width = 140,
                                              )
                                              # icon=flet.Icons.FILE_OPEN_ROUNDED,
                                              #icon_color=orange)

        super().__init__(
            content=flet.Column(controls=[self.rail, self.doc_button], spacing=10),
            padding=flet.padding.all(15),
            margin=flet.margin.all(0),
            width=140,
            bgcolor=white,
            visible=self.nav_rail_visible,
        )

    def open_html_documentation(self, e):
        html_file_path = "site/index.html"
        self.page.launch_url(html_file_path)

    def handle_profile_button(self, x):
        def change_password(e):
            old_password = dialog_field.controls[0].value
            new_password = dialog_field.controls[1].value
            repeat_password = dialog_field.controls[2].value

            if User.get_user_password(old_password):  # if old password is correct
                if new_password == repeat_password:
                    if len(new_password) < 8:
                        dialog_field.controls[1].value = ""
                        dialog_field.controls[2].value = ""
                        dialog_field.controls[1].error_text = "Пароль должен содержать не менее 8 символов"
                        self.page.update()
                        return

                    if not User.change_password(new_password):
                        self.error_text.visible = True
                        return

                    print("successfully change password")
                elif old_password == new_password:
                    dialog_field.controls[1].value = ""
                    dialog_field.controls[2].value = ""
                    dialog_field.controls[1].error_text = "Новый пароль совпадает с текущим"
                    self.page.update()
                    return
                else:
                    dialog_field.controls[1].value = ""
                    dialog_field.controls[2].value = ""
                    dialog_field.controls[1].error_text = "Пароли не совпадают"
                    dialog_field.controls[2].error_text = "Пароли не совпадают"
                    self.page.update()
                    return
            else:
                dialog_field.controls[0].error_text = "Неверный текущий пароль "
                dialog_field.controls[1].value = ""
                dialog_field.controls[2].value = ""
                self.page.update()
                return

            self.page.close(dialog)
            self.page.update()

            snackbar = flet.SnackBar(flet.Text("Пароль успешно изменен ;)"))
            e.control.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

        def on_click(e):
            print('a')
            self.error_text.visible = False
            dialog_field.controls[0].error_text = None
            dialog_field.controls[1].error_text = None
            dialog_field.controls[2].error_text = None
            self.page.update()

        dialog_field = (
            flet.Column(
                [flet.TextField(bgcolor=white, label="Текущий пароль:", width=350, color="black",
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
            self.prev_nav = self.rail.selected_index
        elif index == 1:
            self.page.route = "/clock"
            self.prev_nav = self.rail.selected_index
        elif index == 2:
            self.app_layout.set_reset_view()

            # self.page.route = "/reset"
        elif index == 4:
            self.page.route = "/info"
            self.prev_nav = self.rail.selected_index

        self.page.update()
