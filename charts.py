import math

import flet
from flet import canvas

from datetime import datetime
import calendar

from reportlab.lib.pdfencrypt import padding

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"
green = "#59A343"

# chart for info about battery life
class BarChart:
    def __init__(self, value):
        # self.page = page

        if value >= 2500:
            self.color = green
        elif 2400 <= value < 2500:
            self.color = "yellow"
        elif 2000 <= value < 2400:
             self.color = "red"
        else:
            self.color = "#333333"

        self.bg_color = "white"
        self.max_value = 3100
        self.border_radius = 28
        self.value = value
        self.height = 22
        self.width = 516

        self.chart = (
            flet.Stack([
                flet.Container(
                    width=self.width,
                    height=self.height,
                    bgcolor=self.bg_color,
                    border_radius=28
                ),
                flet.Container(
                    width= self.width * self.value / self.max_value,
                    height = self.height,
                    bgcolor=self.color,
                    border_radius=28,
                    animate=flet.Animation(300, flet.AnimationCurve.LINEAR),
                    # on_hover=self.animate
                ),
                flet.Text(f"{self.value}/{self.max_value} мВ",
                          color=white if self.value > 1800 else "#333333",
                          size=18,
                          weight=flet.FontWeight.W_600,
                          left=187),
            ], alignment=flet.alignment.center_left)
        )

    def animate(self, e):
        self.chart.controls[1].width = self.width * self.value / self.max_value -20 \
            if self.chart.controls[1].width == self.width * self.value / self.max_value\
            else self.width * self.value / self.max_value

        self.chart.update()

class Curve:
    def __init__(self, color, value):
        self.color = color
        self.max_value = math.pi
        self.value = value * self.max_value / 100
        print(self.value)

        self.chart = (
            flet.Container(
                canvas.Canvas(
                    [
                    canvas.Arc(
                        x=0,
                        y=0,
                        width=200,
                        height=200,
                        start_angle=-math.pi,
                        sweep_angle=math.pi,
                        paint=flet.Paint(
                            stroke_width=40,
                            style=flet.PaintingStyle.STROKE,
                            stroke_cap=flet.StrokeCap.ROUND,
                            # stroke_dash_pattern = [5,10],
                            color="#C5C5C5",
                        ),
                    ),
                    #Дуга синим цветом
                    canvas.Arc(
                        x=0,
                        y=0,
                        width=200,
                        height=200,
                        start_angle=-math.pi,  # от вертикали вверх
                        sweep_angle=self.value,  # половина окружности
                        paint=flet.Paint(
                            stroke_width=40,
                            style=flet.PaintingStyle.STROKE,  # только контур
                            stroke_cap=flet.StrokeCap.ROUND,
                            color=self.color,
                        ),
                    ),
                    ],
                width = 200,
                height = 200,
                ),
            padding=0,
            width=235,
            height=125,
            alignment=flet.alignment.bottom_left,
            # expand=True
            )
        )

class Calendar:

    month = {1 : "Январь",
             2 : "Февраль",
             3 : "Март",
             4 : "Апрель",
             5 : "Май",
             6 : "Июнь",
             7 : "Июль",
             8 : "Август",
             9 : "Сентябрь",
             10 : "Октябрь",
             11 : "Ноябрь",
             12 : "Декабрь"}

    def __init__(self,app, page, date_field):
        self.app = app
        self.page = page
        self.date_field = date_field
        # Контейнер для дней
        self.days_grid = flet.GridView(
            expand=True,
            max_extent=50,
            child_aspect_ratio=1.0,
            padding=4,
            spacing=1,
            run_spacing=1,
            width=338,
            height=233,
            # auto_scroll=False
        )

        # self.today = datetime.today()
        self.today = datetime.strptime(self.date_field.value, "%d.%m.%Y")

        self.selected_date = flet.Ref()
        self.current_month = flet.Ref()
        self.current_year = flet.Ref()

        self.selected_date_label = flet.Text(color="black", size=15) # -> to ClockView

        # Метка текущего месяца
        self.month_label = flet.Text(f"{Calendar.month[self.today.month]} {self.today.year}", color="black",
                                     weight=flet.FontWeight.W_600, size=15)

        self.nav_row = self.calendar()

        self.layout = ( # -> to ClockView
            flet.Container(
                flet.Column([
                    # self.selected_date_label,
                    self.nav_row,
                    self.days_grid,
                ],spacing=-10),
                width=370,
                height=316,
                bgcolor="#D9D9D9",
                # alignment=flet.alignment.top_left,
                padding = flet.Padding(18,0,18,0)
            )
        )
        self.update_calendar(self.today.year, self.today.month)


    def calendar(self):
        self.today = datetime.today()
        # self.selected_date = flet.Ref()
        self.selected_date.current = self.today  # выбранная дата

        # Label для отображения выбранной даты
        self.selected_date_label.value = self.today.strftime('%d.%m.%Y')
        self.date_field.value = self.selected_date_label.value

        # # Обновление сетки календаря для выбранного месяца
        # def update_calendar(year, month):
        #     self.days_grid.controls.clear()
        #     # заголовки дней недели
        #     for day_name in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        #         self.days_grid.controls.append(flet.Container(
        #             content=flet.Text(day_name, weight=flet.FontWeight.BOLD),
        #             alignment=flet.alignment.center,
        #
        #         ))
        #
        #     month_calendar = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
        #     for week in month_calendar:
        #         for day in week:
        #             if day == 0:
        #                 # пустые дни
        #                 self.days_grid.controls.append(flet.Container())
        #             else:
        #                 day_date = datetime(year, month, day)
        #                 # подсветка выбранного дня
        #                 # is_today = day_date.date() == today.date()
        #                 btn = flet.ElevatedButton(
        #                     text=str(day),
        #                     # bgcolor={ft.ControlState.DEFAULT:None,
        #                     #          ft.ControlState.PRESSED:"green"},
        #                     bgcolor="green" if self.selected_date.current.strftime('%d') == day_date.strftime(
        #                         '%d') else None,
        #                     on_click=lambda e, d=day_date: select_day(d)
        #                 )
        #                 self.days_grid.controls.append(btn)
        #     self.page.update()

        # # Функция выбора дня
        # def select_day(day_date):
        #     self.selected_date.current = day_date
        #     self.selected_date_label.value = day_date.strftime('%d.%m.%Y')
        #     # btn.bgcolor = "green" if  day_date.date() == today.date() else None
        #
        #     self.update_calendar(int(day_date.strftime('%Y')), int(day_date.strftime('%m')))
        #
        #     self.page.update()

        # Навигация по месяцам
        # current_month = flet.Ref()
        self.current_month.current = self.today.month
        # current_year = flet.Ref()
        self.current_year.current = self.today.year

        def prev_month(e):
            if self.current_month.current == 1:
                self.current_month.current = 12
                self.current_year.current -= 1
            else:
                self.current_month.current -= 1
            self.update_calendar(self.current_year.current, self.current_month.current)
            self.month_label.value = f"{Calendar.month[self.current_month.current]} {self.current_year.current}"
            self.page.update()

        def next_month(e):
            if self.current_month.current == 12:
                self.current_month.current = 1
                self.current_year.current += 1
            else:
                self.current_month.current += 1
            self.update_calendar(self.current_year.current, self.current_month.current)
            self.month_label.value = f"{Calendar.month[self.current_month.current]} {self.current_year.current}"
            self.page.update()

        # Метка текущего месяца
        # month_label = flet.Text(f"{today.year}-{today.month:02d}", size=18)

        # # Кнопки навигации
        # self.nav_row = flet.Row([
        #     flet.IconButton(flet.Icons.ARROW_BACK, on_click=prev_month),
        #     month_label,
        #     flet.IconButton(flet.Icons.ARROW_FORWARD, on_click=next_month)
        # ], alignment=flet.MainAxisAlignment.CENTER, spacing=20)

        # page.add(
        #     selected_label,
        #     self.nav_row,
        #     self.days_grid
        # )

        # Инициализация календаря
        # self.update_calendar(self.today.year, self.today.month)

        return (
            flet.Row([
                self.month_label,
                flet.Row([
                    flet.IconButton(flet.Icons.ARROW_BACK_IOS_ROUNDED, on_click=prev_month, icon_color=orange),
                    flet.IconButton(flet.Icons.ARROW_FORWARD_IOS_ROUNDED, on_click=next_month, icon_color=orange)
                ])
            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN,)
        )


    # Функция выбора дня
    def select_day(self,day_date):
        self.selected_date.current = day_date
        self.selected_date_label.value = day_date.strftime('%d.%m.%Y')
        self.date_field.value = self.selected_date_label.value

        self.update_calendar(int(day_date.strftime('%Y')), int(day_date.strftime('%m')))

        self.page.update()

    # Обновление сетки календаря для выбранного месяца
    def update_calendar(self, year, month):
        self.days_grid.controls.clear()
        # заголовки дней недели
        for day_name in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            self.days_grid.controls.append(
                flet.Container(
                    content=flet.Text(day_name, color="black", size=13),
                    alignment=flet.alignment.center,
                )
            )

        month_calendar = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
        for week in month_calendar:
            for day in week:
                if day == 0:
                    # пустые дни
                    self.days_grid.controls.append(flet.Container())
                else:
                    day_date = datetime(year, month, day)

                    # подсветка выбранного дня
                    # is_today = day_date.date() == today.date()
                    btn = flet.FilledTonalButton(
                        content=flet.Text(str(day), color=orange if day_date.date() == self.today.date()
                                                                 else "black",
                                                    size=19 if day_date.date() == self.today.date()
                                                                 else 17,
                                                    weight=flet.FontWeight.W_600 if day_date.date() == self.today.date()
                                                                 else flet.FontWeight.NORMAL),
                        width=44, height=44,
                        bgcolor="#DFCEBE" if self.selected_date.current.date() == day_date.date() else "#D9D9D9",
                        on_click=lambda e, d=day_date: self.select_day(d)
                    )
                    self.days_grid.controls.append(btn)
        self.page.update()


    # def calendar(self, page: flet.Page):
    #     today = datetime.today()
    #     selected_date = flet.Ref[datetime]()
    #     selected_date.current = today  # выбранная дата
    #
    #     # Label для отображения выбранной даты
    #     selected_label = flet.Text(f"Выбрана дата: {today.strftime('%Y-%m-%d')}", size=18)
    #
    #     # Обновление сетки календаря для выбранного месяца
    #     def update_calendar(year, month):
    #         self.days_grid.controls.clear()
    #         # заголовки дней недели
    #         for day_name in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
    #             self.days_grid.controls.append(flet.Container(
    #                 content=flet.Text(day_name, weight=flet.FontWeight.BOLD),
    #                 alignment=flet.alignment.center,
    #
    #             ))
    #
    #         month_calendar = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
    #         for week in month_calendar:
    #             for day in week:
    #                 if day == 0:
    #                     # пустые дни
    #                     self.days_grid.controls.append(flet.Container())
    #                 else:
    #                     day_date = datetime(year, month, day)
    #                     # подсветка выбранного дня
    #                     # is_today = day_date.date() == today.date()
    #                     btn = flet.ElevatedButton(
    #                         text=str(day),
    #                         # bgcolor={ft.ControlState.DEFAULT:None,
    #                         #          ft.ControlState.PRESSED:"green"},
    #                         bgcolor="green" if selected_date.current.strftime('%d') == day_date.strftime(
    #                             '%d') else None,
    #                         on_click=lambda e, d=day_date: select_day(d)
    #                     )
    #                     self.days_grid.controls.append(btn)
    #         self.page.update()
    #
    #     # Функция выбора дня
    #     def select_day(day_date):
    #         selected_date.current = day_date
    #         selected_label.value = f"Выбрана дата: {day_date.strftime('%d.%m.%Y')}"
    #         # btn.bgcolor = "green" if  day_date.date() == today.date() else None
    #
    #         update_calendar(int(day_date.strftime('%Y')), int(day_date.strftime('%m')))
    #
    #         page.update()
    #
    #     # Навигация по месяцам
    #     current_month = flet.Ref()
    #     current_month.current = today.month
    #     current_year = flet.Ref()
    #     current_year.current = today.year
    #
    #     def prev_month(e):
    #         if current_month.current == 1:
    #             current_month.current = 12
    #             current_year.current -= 1
    #         else:
    #             current_month.current -= 1
    #         update_calendar(current_year.current, current_month.current)
    #         month_label.value = f"{current_year.current}-{current_month.current:02d}"
    #         self.page.update()
    #
    #     def next_month(e):
    #         if current_month.current == 12:
    #             current_month.current = 1
    #             current_year.current += 1
    #         else:
    #             current_month.current += 1
    #         update_calendar(current_year.current, current_month.current)
    #         month_label.value = f"{current_year.current}-{current_month.current:02d}"
    #         self.page.update()
    #
    #     # Метка текущего месяца
    #     month_label = flet.Text(f"{today.year}-{today.month:02d}", size=18)
    #
    #     # Кнопки навигации
    #     self.nav_row = flet.Row([
    #         flet.IconButton(flet.Icons.ARROW_BACK, on_click=prev_month),
    #         month_label,
    #         flet.IconButton(flet.Icons.ARROW_FORWARD, on_click=next_month)
    #     ], alignment=flet.MainAxisAlignment.CENTER, spacing=20)
    #
    #     page.add(
    #         selected_label,
    #         self.nav_row,
    #         self.days_grid
    #     )
    #
    #     # Инициализация календаря
    #     update_calendar(today.year, today.month)