import asyncio

import flet
import datetime
import subprocess
from flask import Flask, request

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

now = datetime.datetime.now()

# time = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"

class ClockView(flet.Container):
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.date_field = flet.TextField(value= self.get_date(),border= flet.InputBorder.NONE, color= "black")
        self.time_field = flet.TextField(border= flet.InputBorder.NONE, color="black")

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
                                self.date_field,
                                self.time_field
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
                            flet.TextField(value=self.get_time_zone(), border=flet.InputBorder.NONE, color="black")

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

        self.get_time()


    def get_date(self):
        # date = datetime.date.today().strftime("%d.%m.%Y")
        # date = 3

        now = datetime.datetime.now()
        formatted_date = f"{now.day:02d}.{now.month:02d}.{now.year}"

        # self.get_time()

        return formatted_date

    def get_time(self):
        async def update_time():
            # global time
            while True:
                # time_now = datetime.datetime.now()

                self.time_field.value = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
                self.app.page.update()

                await asyncio.sleep(1)

        self.app.page.run_task(update_time)


    def get_time_zone(self):
        time_zone = subprocess.run(["date", '+%Z %z'], capture_output=True, text=True, check= True)
        return time_zone.stdout

    # TODO:
    #  formatting time
    #  updating time every second
    #  reading and setting time zones
    #  setting NTP and choosing servers (list)
    #  button edit (add ability to change date/time values)
    # def set_time(self):
    # def set_date(self):
    # def set_ntp_server(self):
