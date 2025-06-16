import flet
from reportlab.lib.pdfencrypt import padding

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"

class Sidebar(flet.Container):

    def __init__(self, app_layout):
        # self.store: DataStore = store
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            flet.NavigationRailDestination(
                icon=flet.Icons.CAST_CONNECTED,
                selected_icon=flet.Icons.CAST_CONNECTED,
                # label="Настройка сети",
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
        ]

        # self.top_nav_rail = ft.NavigationRail( # destinations "Boards" and "Members"
        #     selected_index=None,
        #     label_type=ft.NavigationRailLabelType.ALL,
        #     on_change=self.top_nav_change,
        #     destinations=self.top_nav_items,
        #     bgcolor=ft.Colors.BLUE_GREY,
        #     extended=True,
        #     height=110,
        # )

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
                        content=flet.Text("AB"),
                    ),
                    controls=[
                        flet.Container(
                            content=flet.CupertinoButton(
                                "Профиль",
                                opacity_on_click=0.3,
                                on_click=lambda e: print("Профиль"),
                                color="black",
                                icon=flet.Icons.ACCOUNT_CIRCLE,
                                icon_color="black"
                            ),
                            bgcolor="#CACACA",
                            padding=0,
                            width=140,
                        ),
                        flet.Container(
                            content=flet.ElevatedButton("Выйти", on_click=lambda e: print("logout"), bgcolor="red",
                                                        color=white, width=10, ),
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
            # expand=True
        )
        # self.toggle_nav_rail_button = ft.IconButton(ft.Icons.ARROW_BACK)

        super().__init__(
            content=flet.Column(controls=[self.rail]),
            padding=flet.padding.all(15),
            margin=flet.margin.all(0),
            width=140,
            bgcolor=white,
            visible=self.nav_rail_visible,
        )

    def nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        # self.bottom_nav_rail.selected_index = None
        self.rail.selected_index = index
        print(f"index = {index}")
        if index == 0:
            self.page.route = "/settings"
        elif index == 1:
            self.page.route = "/clock"
        self.page.update()