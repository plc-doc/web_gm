import math

import flet
import flet as ft
from flet import canvas


def main(page: ft.Page):

    from system_info_view import InfoView
    #
    page.bgcolor = "#EAEAEA"
    #
    info = InfoView(True, page)
    layout = info.layout
    page.add(layout)
    # info.bar.animate
    page.update()
#


#
#
ft.app(main, view=flet.WEB_BROWSER)


# import flet as ft
#
# def main(page: ft.Page):
#     page.title = "Горизонтальный BarChart (UI)"
#
#     data = [
#         ("Python", 90),
#         ("C++", 70),
#         ("JavaScript", 50),
#         ("Go", 40),
#     ]
#
#     bars = []
#     max_value = max(v for _, v in data)
#
#     for label, value in data:
#         percent = value / max_value * 100
#         bars.append(
#             ft.Row(
#                 [
#                     ft.Text(label, width=100),
#                     ft.Container(
#                         width=percent * 3,  # масштаб ширины
#                         height=25,
#                         bgcolor="blue",
#                         border_radius=5,
#                     ),
#                     ft.Text(f"{value}"),
#                 ],
#                 alignment=ft.MainAxisAlignment.START,
#             )
#         )
#
#     page.add(ft.Column(bars, spacing=10))
# ft.app(main, view=ft.WEB_BROWSER)
#
# import flet as ft

# def main(page: ft.Page):
#
#     c = ft.Container(
#         width=100,
#         height=100,
#         bgcolor="blue",
#         border_radius=5,
#         scale=ft.Scale(scale=1),
#         animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
#     )
#
#     def animate(e):
#         c.scale = 2
#         page.update()
#
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.spacing = 30
#     page.add(
#         c,
#         ft.ElevatedButton("Animate!", on_click=animate),
#     )



# def main(page: ft.Page):
#     page.title = "AnimatedSwitcher examples"
#
#     c1 = ft.Container(
#         ft.Text("Hello!", size=50),
#         alignment=ft.alignment.center,
#         width=200,
#         height=200,
#         bgcolor=ft.Colors.GREEN,
#     )
#     c2 = ft.Container(
#         ft.Text("Bye!", size=50),
#         alignment=ft.alignment.center,
#         width=200,
#         height=200,
#         bgcolor=ft.Colors.GREEN,
#     )
#     c = ft.AnimatedSwitcher(
#         c1,
#         transition=ft.AnimatedSwitcherTransition.SCALE,
#         duration=1000,
#         reverse_duration=100,
#         # switch_in_curve=ft.AnimationCurve.LINEAR,
#         # switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
#     )
#
#     def scale(e):
#         c.content = c2 if c.content == c1 else c1
#         c.transition = ft.AnimatedSwitcherTransition.SCALE
#         c.update()
#
#     def fade(e):
#         c.content = c2 if c.content == c1 else c1
#         c.transition = ft.AnimatedSwitcherTransition.FADE
#         c.update()
#
#     def rotate(e):
#         c.content = c2 if c.content == c1 else c1
#         c.transition = ft.AnimatedSwitcherTransition.ROTATION
#         c.update()
#
#     page.add(
#         c,
#         ft.ElevatedButton("Scale", on_click=scale),
#         ft.ElevatedButton("Fade", on_click=fade),
#         ft.ElevatedButton("Rotate", on_click=rotate),
#     )
#
#
# ft.app(main, view=ft.WEB_BROWSER)

