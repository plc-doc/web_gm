import asyncio

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

        self.date_field = flet.TextField(value= self.get_date(),border= flet.InputBorder.NONE, color= "black")
        self.time_field = flet.TextField(border= flet.InputBorder.NONE, color="black")

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
        self.button = flet.FilledTonalButton(text="Синхронизировать с компьютером",
                                                  bgcolor=orange,
                                                  color="black",
                                                  # on_click=self.stop()
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
                            self.button
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
        self.button.on_click = lambda e: self.stop_time()
        self.time_field.on_click = lambda e: self.time_changed(e)
        self.date_field.on_click = lambda e: self.date_changes(e)

    def time_changed(self, e):
        global task

        self.stop_time()
        self.time_field.filled = True
        self.time_field.bgcolor = white
        self.time_field.border_radius = 14
        self.time_field.width = 14

        self.page.update()

    def date_changes(self, e):
        self.date_field.filled = True
        self.date_field.bgcolor = white
        self.date_field.border_radius = 14
        self.date_field.width = 14

        self.page.update()

    def stop_time(self):
        global task

        task.cancel()
        self.page.update()

    def get_date(self):
        # date = datetime.date.today().strftime("%d.%m.%Y")
        # date = 3

        now = datetime.datetime.now()
        formatted_date = f"{now.day:02d}.{now.month:02d}.{now.year}"

        # self.get_time()

        return formatted_date

    def get_time(self):
        global task
        async def update_time():
            # global time
            while True:
                now = datetime.datetime.now()

                self.time_field.value = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
                self.page.update()
                await asyncio.sleep(1)

        task = self.page.run_task(update_time)



    def get_time_zone(self):
        time_zone = subprocess.run(["date", '+%Z %z'], capture_output=True, text=True, check= True)
        return time_zone.stdout

    # TODO:
    #  setting time zones
    #  setting NTP and choosing servers (list)
    #  button edit (add ability to change date/time values)
    # def set_time(self):
    # def set_date(self):
    # def set_ntp_server(self):
