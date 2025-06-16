import flet
import datetime

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"


class ClockView(flet.Container):
    def __init__(self, app, page):
        self.app = app
        self.page = page

        super().__init__(
            flet.Column(
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
                                flet.TextField(value= self.get_date(),border= flet.InputBorder.NONE, color= "black"),
                                flet.TextField(value= str(self.get_time()), border= flet.InputBorder.NONE, color="black")
                            ], horizontal_alignment=flet.CrossAxisAlignment.CENTER),
                            flet.FilledTonalButton(text="Синхронизировать с компьютером",
                                                  bgcolor=orange,
                                                  color="black",
                                                  on_click=lambda e: print()
                                                   )
                        ], alignment=flet.MainAxisAlignment.SPACE_EVENLY),
                        flet.VerticalDivider(width= 946, color= "#ACACAC"),
                        flet.Row([
                            flet.Text("Часовой пояс", color="black"),

                        ], alignment=flet.MainAxisAlignment.CENTER, spacing= 30)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
                ),
                flet.Container(bgcolor="#CACACA",
                    padding= 20,
                    width=1050,
                    height=293,
                    border_radius=30,
                    alignment=flet.alignment.center,
                    content=flet.Column([
                        flet.Text("Синхронизация времени", color="black", size=18),
                        flet.Row([
                            flet.Column([
                                flet.Text("Синхронизация времени при помощи NTP", color="black"),
                                flet.Text("NTP - серверы", color= "black")
                            ], horizontal_alignment=flet.CrossAxisAlignment.END, spacing= 30),
                            flet.Column([
                                flet.CupertinoSwitch(value= False, active_color=orange),

                            ], horizontal_alignment=flet.CrossAxisAlignment.START, spacing= 30)
                        ], alignment=flet.MainAxisAlignment.SPACE_EVENLY)
                    ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing= 30)
                )
            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER
            ),
            expand=True,
            padding=20
        )


    def get_date(self):
        date = datetime.date.today().strftime("%d.%m.%Y")
        # date = 3
        return date

    def get_time(self):
        time = datetime.datetime.now().time()

        return time