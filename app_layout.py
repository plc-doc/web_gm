import asyncio
from datetime import datetime
from ipaddress import ip_address

import flet
import subprocess

import flet.canvas as cv
import math

from sidebar import Sidebar
from interfaces import Interface
from clock_view import ClockView

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class AppLayout(flet.Row):
    def __init__(self, app, page: flet.Page, *args, **kwargs):
        super().__init__(*args, **kwargs) #calling Row (creating right side of page)
        self.app = app
        self.page: flet.Page = page
        self.sidebar = Sidebar(self) # creating sidebar

        self.eth0 = Interface("Eth0", "abcd.abcd.abcd.abcd", "255.255.255.0", self, self.page)
        self.eth1 = Interface("Eth1", "abcd.abcd.abcd.abcd", "255.255.255.1", self, self.page)
        self.eth2 = Interface("Eth2", "abcd.abcd.abcd.abcd", "255.255.255.2", self, self.page)
        self.eth3 = Interface("Eth3", "abcd.abcd.abcd.abcd", "255.255.255.3", self, self.page)

        paint = flet.Paint(stroke_width= 4, color= orange)

        # self.eth_info0 = (
        #     flet.Column(
        #         controls= [flet.Text(value= "Eth0", color= "black"),
        #                    flet.Card(
        #                         content=flet.Container(
        #                             content=flet.Column(
        #                                 controls=[
        #                                     flet.Row(
        #                                         controls =
        #                                         [flet.Column(
        #                                             controls =[
        #                                                 flet.Text(value= "IP-адрес(IPv4)", color= "black"),
        #                                                 flet.Text(value= "mac адрес",color= "black"),
        #                                                 flet.Text(value= "IP-адрес(IPv6)",color="black")],
        #                                             horizontal_alignment= flet.CrossAxisAlignment.START
        #                                         ),
        #                                         flet.Column(
        #                                             controls=[
        #                                                 flet.Text(value="192.168.1.42",color="black"),
        #                                                 flet.Text(value="255.255.255.0",color="black"),
        #                                                 flet.Text(value="192.168.1.42",color="black")],
        #                                             alignment=flet.MainAxisAlignment.START,
        #                                         ),
        #                                         ],
        #                                         alignment=flet.MainAxisAlignment.CENTER,
        #                                         spacing= 40,
        #                                     ),
        #                                     flet.Row(
        #                                         controls = [
        #                                             flet.FilledTonalButton(
        #                                                 text= "Настроить",
        #                                                 icon=flet.Icons.SETTINGS,
        #                                                 bgcolor= orange,
        #                                                 color= "black",
        #                                                 on_click=self.app.open_ip_settings,
        #                                                 icon_color="black"),],
        #                                         alignment=flet.MainAxisAlignment.END,
        #                                     ),
        #                                 ],
        #                                 horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        #                                 alignment=flet.MainAxisAlignment.CENTER,
        #                                 spacing= 20
        #                             ),
        #                             width=282,
        #                             height=161,
        #                             padding=10,
        #                             bgcolor=white,
        #                             border_radius=20,
        #                         ),
        #                         color=white,
        #                         shadow_color="black",
        #                    ),
        #         ],
        #         spacing= 5,
        #         horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        #         alignment=flet.MainAxisAlignment.CENTER,
        #     )
        # )
        #


        self.clock_view = ClockView(self, self.page)
        self.net_settings_view = (
            flet.Column(
                [
                flet.Text(
                    "Настройка интерфейсов",
                    text_align=flet.alignment.center,
                    color=orange,
                    size=20
                ),
                flet.Stack([
                    flet.Container(
                        bgcolor="#CACACA",
                        width=1343,
                        height=803,
                        border_radius=30,
                        alignment=flet.alignment.center,
                        content=
                            flet.Row(
                                spacing=137,
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.Column(
                                        controls=[self.eth0.info_structure(),
                                                  self.eth1.info_structure(),
                                                  self.eth2.info_structure()
                                                  ],
                                        alignment=flet.MainAxisAlignment.CENTER,
                                        spacing=80
                                    ),
                                    flet.Image(
                                        src=f"GMB.png",
                                        width=343,
                                        height=558,
                                        fit=flet.ImageFit.CONTAIN
                                    ),
                                    self.eth3.info_structure()
                                ],
                            )
                    ),
                    cv.Canvas(
                        [
                            cv.Line(358, 213, x2=625, y2=416, paint=paint),
                            cv.Line(358, 485, x2=625, y2=511, paint=paint),
                            cv.Line(359, 617, x2=627, y2=579, paint=paint),
                            cv.Line(809, 255, x2=985, y2=340, paint=paint),
                        ],
                    )
                ]),

                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                alignment=flet.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

        self._active_view: flet.Control = self.net_settings_view # what we see on page right now

        self.controls = [self.sidebar, flet.VerticalDivider(width=0, color= "#CACACA"), self.active_view]

    # def get_ip4(self):
    #     result = subprocess.run(["ifconfig eth2| grep 'inet' | cut -d: -f2 | awk '{print $2}'"], shell=True,
    #                             capture_output=True, text=True, check=True)
    #     return result.stdout

    @property
    def active_view(self):  # change active view
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        # self.sidebar.sync_board_destinations()
        self.page.update()

    def set_net_settings_view(self):
        self.active_view = self.net_settings_view
        # self.sidebar.bottom_nav_rail.selected_index = i
        self.sidebar.rail.selected_index = 0
        # self.page_resize()
        self.page.update()

    def update_net_settings(self):
        self.net_settings_view.update()
        self.set_net_settings_view()

    def set_clock_view(self):
        self.active_view = self.clock_view
        self.sidebar.rail.selected_index = 1
        # self.sidebar.bottom_nav_rail.selected_index = None
        self.page.update()

    # def open_ip_settings(self, e):
    #     global number
    #
    #     print("opened")
    #     def close_dlg(e):
    #         # if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
    #         #     type(e.control) is flet.TextField and e.control.value != ""
    #         # ):
    #         #     self.create_new_board(dialog_text.value)
    #         # self.page.close(dialog)
    #         # self.page.update()
    #         print("clicked")
    #
    #     # def textfield_change(e):
    #         # if dialog_text.value == "":
    #         #     create_button.disabled = True
    #         # else:
    #         #     create_button.disabled = False
    #         # self.page.update()
    #         # print(dialog_text.value)
    #
    #
    #
    #     ip_address_field = flet.TextField(value = "192.168.0.0",bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
    #                                       cursor_color= orange, height=40, width=250, fill_color=white, text_size=14, disabled = True)
    #     mask_field = flet.TextField(value = "255.255.255.0",bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
    #                                 cursor_color=orange, height=40, width=250, fill_color=white, text_size=14, disabled = True)
    #
    #     def ipv6_changed(e):
    #         selected = e.control.value
    #         print(selected)
    #
    #         if selected == "Вручную":
    #             container.content = (
    #                 flet.Column([
    #                     flet.Row([
    #                         flet.Column([
    #                             flet.Text(value="IP-адрес", color="black"),
    #                             flet.Text(value="Маска подсети", color="black")
    #                         ]),
    #                         flet.Column([
    #                             flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
    #                                 cursor_color=orange,
    #                                            height=40,
    #                                            width=250, fill_color=white, text_size=14),
    #                             flet.TextField(value= "0.0.0.0", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
    #                                 cursor_color=orange,
    #                                            height=40,
    #                                            width=250, fill_color=white, text_size=14)
    #                         ])
    #                     ])
    #                 ])
    #             )
    #
    #         elif container.content is not None:
    #             container.content.clean()
    #         self.page.update()
    #
    #     def ipv4_changed(e):
    #         selected = e.control.value
    #         print(selected)
    #
    #         if selected == "Вручную":
    #             ip_address_field.disabled = False
    #             ip_address_field.value = "0.0.0.0"
    #             mask_field.disabled = False
    #             mask_field.value = "0.0.0.0"
    #
    #         else:
    #             ip_address_field.disabled = True
    #             ip_address_field.value = "192.168.0.0"
    #             mask_field.disabled = True
    #             mask_field.value = "255.255.255.0"
    #         self.page.update()
    #
    #     container = flet.Container()
    #     container_4 = flet.Container(
    #                         flet.Column([
    #                             flet.Row([
    #                                 flet.Column([
    #                                     flet.Text(value="IP-адрес", color="black"),
    #                                     flet.Text(value="Маска подсети", color="black")
    #                                 ]),
    #                                 flet.Column([
    #                                     ip_address_field,
    #                                     mask_field
    #                                 ])
    #                             ], spacing = 55)
    #                         ])
    #     )
    #
    #     mac_address = flet.TextField(value="hello", bgcolor=white, border_radius=14, focused_border_color=orange, selection_color = orange, color="black",
    #                                 cursor_color=orange, height=40, width=250, fill_color=white, text_size=14)
    #     button_cancel = flet.ElevatedButton(text="Отменить изменения", color=orange, bgcolor="white", width=209,
    #                                         height=28, on_click=lambda e: print(mac_address.value), )
    #     button_save = flet.ElevatedButton(text="Применить", color="black", bgcolor=orange, width=137, height=28,
    #                                       on_click=lambda e: print(mac_address.value), disabled = False)
    #
    #     fields = flet.Column([
    #                     flet.Text(color="black"),
    #                     flet.Row([
    #                         flet.Row([
    #                             flet.Text(value= "Конфигурация IPv4", color= "black"),
    #                             flet.Dropdown(
    #                                 value = "Использовать DHCP",
    #                                 width=240,
    #                                 options=[
    #                                     flet.dropdown.Option("Использовать DHCP"),
    #                                     flet.dropdown.Option("Использовать BOOTP"),
    #                                     flet.dropdown.Option("Вручную")
    #                                 ],
    #                                 border_radius=10,
    #                                 color="black",
    #                                 text_size=14,
    #                                 bgcolor=orange,
    #                                 border_color="black",
    #                                 focused_border_color=orange,
    #                                 on_change=ipv4_changed,
    #                             ),
    #                             ],spacing= 30,),
    #                         flet.Row([
    #                             flet.Text(value= "Конфигурация IPv6", color= "black"),
    #                             flet.Dropdown(
    #                                 value = "Использовать DHCP",
    #                                 width=240,
    #                                 options=[
    #                                     flet.dropdown.Option("Использовать DHCP"),
    #                                     flet.dropdown.Option("Использовать BOOTP"),
    #                                     flet.dropdown.Option("Вручную"),
    #                                 ],
    #                                 border_radius=10,
    #                                 color= "black",
    #                                 text_size= 14,
    #                                 bgcolor=orange,
    #                                 border_color="black",
    #                                 focused_border_color=orange,
    #                                 on_change=ipv6_changed
    #                             ),
    #                         ],spacing= 30,),
    #                     ],alignment=flet.MainAxisAlignment.CENTER,spacing= 100),
    #                     flet.Row([container_4, container], alignment= flet.MainAxisAlignment.SPACE_BETWEEN, spacing= 85), #Появляющееся окно ручной настройки
    #                     flet.Row([
    #                         flet.Text(value= "mac адрес", color= "black"),
    #                         mac_address
    #                     ], alignment=flet.MainAxisAlignment.START, spacing = 85),
    #                     # flet.Row([
    #                     #     button_cancel,
    #                     #     button_save
    #                     # ], alignment=flet.MainAxisAlignment.END, spacing=30)
    #
    #     ],
    #     horizontal_alignment=flet.CrossAxisAlignment.CENTER,
    #     # alignment= flet.MainAxisAlignment.START,
    #     spacing = 30,
    #     # width=100,
    #     height=270,
    #     )
    #
    #     # if number == 0:
    #     #     fields.controls[0].value= f"Интерфейс:   Eth0"
    #     # elif number == 1:
    #     #     fields.controls[0].value= f"Интерфейс:   Eth1"
    #     # elif number == 2:
    #     #     fields.controls[0].value= f"Интерфейс:   Eth2"
    #     # elif number == 3:
    #     #     fields.controls[0].value= f"Интерфейс:   Eth3"
    #
    #     dialog_field =(
    #         flet.Column(controls=[
    #             fields,
    #             flet.Row([
    #                 button_cancel,
    #                 button_save
    #             ], alignment=flet.MainAxisAlignment.END, spacing=30)
    #         ],
    #         alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
    #         spacing= 40
    #         )
    #     )
    #
    #     advanced_settings_4 = (
    #         flet.Container(
    #             content= flet.Column(
    #                 [
    #                 flet.Row([
    #                     flet.Column([
    #                         flet.Text(value="IP-адрес", color="black"),
    #                         flet.Text(value="Маска подсети", color="black")
    #                     ]),
    #                     flet.Column([
    #                         flet.TextField(bgcolor="white", border_radius=20, border_color=orange, color="black",
    #                                        height=40,
    #                                        width=250, fill_color=white, text_size=14),
    #                         flet.TextField(bgcolor="white", border_radius=20, border_color=orange, color="black",
    #                                        height=40,
    #                                        width=250, fill_color=white, text_size=14)
    #                     ])
    #                 ])
    #                 ]
    #             )
    #         )
    #     )
    #
    #     advanced_settings_6 = (
    #         flet.Container(
    #             content= flet.Column([
    #                     flet.Row([
    #                         flet.Column([
    #                             flet.Text(value="IP-адрес", color="black"),
    #                             flet.Text(value="Маска подсети", color="black")
    #                         ]),
    #                         flet.Column([
    #                             flet.TextField(bgcolor="white", border_radius=20, border_color=orange, color="black",
    #                                            height=40,
    #                                            width=250, fill_color=white, text_size=14),
    #                             flet.TextField(bgcolor="white", border_radius=20, border_color=orange, color="black",
    #                                            height=40,
    #                                            width=250, fill_color=white, text_size=14)
    #                         ])
    #                     ])
    #             ])
    #         )
    #     )
    #
    #     # dialog_text = flet.TextField(
    #     #     label="New Board Name", on_submit=close_dlg, on_change=textfield_change
    #     # )
    #     # create_button = flet.ElevatedButton(
    #     #     text="Create", bgcolor=flet.Colors.BLUE_200, on_click=close_dlg, disabled=False
    #     # )
    #
    #     dialog = flet.AlertDialog(
    #         content=flet.Container(
    #             width=900,
    #             height=350,
    #             content=dialog_field
    #         ),
    #         bgcolor=white,
    #         on_dismiss=lambda e: print("Dialog dismissed!"),
    #         content_padding=50,
    #     )
    #     self.page.open(dialog)
    #     dialog.open = True
    #     self.page.update()
    #     # dialog_text.focus()