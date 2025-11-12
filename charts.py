import math

import flet
from flet import canvas
from flet.core.map.polyline_layer import DashedStrokePattern

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"
green = "#59A343"

# chart for info about battery life
class BarChart:
    def __init__(self, value):
        # self.page = page
        self.color = green
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
                    on_hover=self.animate
                ),
                flet.Text(f"{self.value}/{self.max_value} мВ",
                          color=white if self.value > 1800 else "#333333",
                          size=18,
                          weight=flet.FontWeight.W_600,
                          left=187),
            ], alignment=flet.alignment.center_left)
        )

    def animate(self, e):
        # if self.chart.controls[1].width == self.width * self.value / self.max_value:
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
