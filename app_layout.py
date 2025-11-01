import flet

import flet.canvas as cv

from sidebar import Sidebar
from interfaces import Interface
from clock_view import ClockView
from reset_view import ResetView

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class AppLayout(flet.Row):
    def __init__(self, app, page: flet.Page, *args, **kwargs):
        super().__init__(*args, **kwargs) #calling Row (creating right side of page)
        self.app = app
        self.page: flet.Page = page
        self.sidebar = Sidebar(self) # creating sidebar
        # self.page.on_resized = self.page_resize

        self.eth0 = Interface("Eth0", self, self.page, "100")
        self.eth1 = Interface("Eth1", self, self.page, "200")
        self.eth2 = Interface("Eth2", self, self.page, "300")
        self.ecat = Interface("Ecat", self, self.page, "400")

        paint = flet.Paint(stroke_width= 4, color= orange) # orange lines

        self.clock_view = ClockView(self, self.page).container
        self.state_view = flet.Container()
        self.reset_view = ResetView(self, self.page)
        self.net_settings_view = (
            flet.Container(
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
                            padding=54,
                            alignment=flet.alignment.center,
                            content=
                                flet.Row(
                                    spacing=137,
                                    alignment=flet.MainAxisAlignment.CENTER,
                                    vertical_alignment=flet.CrossAxisAlignment.CENTER,
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
                                        self.ecat.info_structure()
                                    ]
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
                # alignment=flet.MainAxisAlignment.CENTER,
                spacing=20,
                # expand=True,
            ),
            padding=20,
            expand=True
            )
        )

        self._active_view: flet.Control = self.net_settings_view # what we see on page right now

        self.controls = [self.sidebar, flet.VerticalDivider(width=0, color= "#CACACA"), self.active_view]


    @property
    def active_view(self):  # change active view
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.page.update()

    def set_net_settings_view(self):
        self.active_view = self.net_settings_view
        self.sidebar.rail.selected_index = 0
        self.page.update()

    # def update_net_settings(self):
    #     self.net_settings_view.update()
    #     self.set_net_settings_view()

    def set_clock_view(self):
        self.active_view = self.clock_view
        self.sidebar.rail.selected_index = 1
        self.page.update()

    def set_reset_view(self):
        self.page.open(self.reset_view)
        self.reset_view.open = True
        self.page.update()

    def set_state_view(self):
        self.active_view = self.state_view
        self.sidebar.rail.selected_index = 4
        self.page.update()


