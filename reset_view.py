import flet

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class ResetView(flet.AlertDialog):
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.params = ["Настройки пользователей", "Настройки CodeSys", "Настройки сетевой\nконфигурации"]

        self.checkbox = flet.CupertinoCheckbox(value=False,
                                                fill_color={flet.ControlState.DISABLED: white,
                                                            flet.ControlState.SELECTED: orange},
                                                border_side={flet.ControlState.DEFAULT:flet.BorderSide(color="black", width=2),
                                                             flet.ControlState.HOVERED: flet.BorderSide(color=orange, width=3),
                                                             flet.ControlState.SELECTED: flet.BorderSide(color=orange, width=15)},
                                                # width=120, height=20,
                                                check_color="white",
                                                on_change=self.click_checkbox
                                               )

        self.chips = []
        for i,param in enumerate(self.params):
            self.chips.append(flet.Chip(label=flet.Text(value=param, size=15, color="black", text_align=flet.TextAlign.CENTER, max_lines=2),
                                        on_select=self.chip_selected,
                                        color={flet.ControlState.DEFAULT: "white", flet.ControlState.SELECTED: orange, flet.ControlState.HOVERED: "#FFF0DF"},
                                        border_side=flet.BorderSide(color=orange, width=2),
                                        shape=flet.RoundedRectangleBorder(radius=13),
                                        elevation=2,
                                        click_elevation=4,
                                        show_checkmark=False,
                                        )
                              )
            if i == 0:
                self.chips[i].padding = flet.padding.Padding(9,19,9,19)
            elif i == 1:
                self.chips[i].padding = flet.padding.Padding(26,19,26,19)
            else:
                self.chips[i].padding = flet.padding.Padding(31,8.5,31,8.5)


        self.content = flet.Column([
                        flet.Text(value="Выберите параметры для сброса",
                                  color="black",
                                  size = 22
                        ),
                        flet.Container(
                            content=flet.Column(controls=[
                                            flet.Row([self.chips[0],
                                                              self.chips[1]], spacing=58,alignment=flet.MainAxisAlignment.CENTER,
                                                     ),

                                            flet.Row([self.chips[2]], alignment=flet.MainAxisAlignment.CENTER),
                                            flet.Row([self.checkbox, flet.Text(value="Bыбрать все", color="black", size=15)],
                                                     alignment=flet.MainAxisAlignment.START, spacing=5
                                                     )
                                    ], alignment=flet.MainAxisAlignment.CENTER, spacing=18),
                            width=536,
                            height=241,
                            bgcolor="#F2F2F2",
                            border_radius=13,
                            padding=flet.padding.Padding(6,0,6,0),
                            shadow=flet.BoxShadow(color="#AAAAAA",
                                                  offset=flet.Offset(-1, 7),
                                                  blur_radius=4,
                                                  spread_radius=1
                                                  )
                        ),
                        flet.Row([
                            flet.TextButton(content=flet.Text("Отменить", color="black", size=17), on_click=self.cancel),
                            flet.TextButton(content=flet.Text("Сбросить", color=orange, size=17, weight=flet.FontWeight.W_600,
                                                              style=flet.TextStyle(letter_spacing=0.3)))
                        ], alignment=flet.MainAxisAlignment.END, spacing=20)
        ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, alignment=flet.MainAxisAlignment.CENTER,
            spacing=20)


        super().__init__(
            content=flet.Container(
                content=self.content,
                bgcolor="white",
                border_radius=13,
                width=549,
                height=408,
                expand=True
            ),
            bgcolor="white",
            content_padding=flet.padding.Padding(35, 0, 35, 0),
        )

    def chip_selected(self, e):
        for chip in self.chips:
            if not chip.selected:
                self.checkbox.value = False
                break
        else:
            self.checkbox.value = True

        self.checkbox.update()
        e.control.update()

    def cancel(self, e):
        self.page.close(self)
        self.page.update()

    def click_checkbox(self, e):
        for chip in self.chips:
            if e.control.value:
                chip.selected = True
            else:
                chip.selected = False
        self.page.update()