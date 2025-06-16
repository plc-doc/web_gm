self.net_settings_view = (
            flet.Column(
                controls= [flet.Text(value= "Настройка интерфейсов",
                                     text_align=flet.alignment.center,
                                     color=orange,
                                     size=20),
                           flet.Container(bgcolor= "#CACACA",
                                          width=1343,
                                          height= 803,
                                          border_radius= 30,
                                          alignment=flet.alignment.center,
                                          content=flet.Row( spacing=137,
                                                            alignment=flet.MainAxisAlignment.CENTER,
                                                            controls=[flet.Column(
                                                                            [flet.Column(
                                                                            [flet.Text(value= "Eth0", color= "black"),
                                                                                    flet.Card(
                                                                                        content=flet.Container(
                                                                                            content=flet.Column(
                                                                                                [flet.Row([
                                                                                                            flet.Column([
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv4)",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "mac адрес",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv6)",
                                                                                                                    color="black"
                                                                                                                )
                                                                                                            ],
                                                                                                            horizontal_alignment= flet.CrossAxisAlignment.START
                                                                                                            ),
                                                                                                            flet.Column(
                                                                                                                [
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="255.255.255.0",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    )
                                                                                                                ],
                                                                                                                alignment=flet.MainAxisAlignment.START,
                                                                                                            ),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.CENTER,
                                                                                                            spacing= 40,
                                                                                                    ),
                                                                                                    flet.Row(
                                                                                                    [flet.FilledTonalButton("Настроить",
                                                                                                                                   icon=flet.Icons.SETTINGS,
                                                                                                                                   bgcolor= orange,
                                                                                                                                   color= "black",
                                                                                                                                   on_click=lambda e: print("k"),
                                                                                                                                   icon_color="black"),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.END,
                                                                                                    ),
                                                                                                ],
                                                                                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                                                                alignment=flet.MainAxisAlignment.CENTER,
                                                                                                spacing= 20
                                                                                            ),
                                                                                            width=282,
                                                                                            height=161,
                                                                                            padding=10,
                                                                                            bgcolor=white,
                                                                                            border_radius=20,
                                                                                        ),
                                                                                        color=white,
                                                                                        shadow_color="black",
                                                                                    ),
                                                                                    ],
                                                                                    spacing= 5,
                                                                                    horizontal_alignment=flet.CrossAxisAlignment.CENTER),
                                                                                    flet.Column(
                                                                                [flet.Text(value= "Eth1", color= "black"),
                                                                                        flet.Card(
                                                                                        content=flet.Container(
                                                                                            content=flet.Column(
                                                                                                [flet.Row([
                                                                                                            flet.Column([
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv4)",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "mac адрес",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv6)",
                                                                                                                    color="black"
                                                                                                                )
                                                                                                            ],
                                                                                                            horizontal_alignment= flet.CrossAxisAlignment.START
                                                                                                            ),
                                                                                                            flet.Column(
                                                                                                                [
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="255.255.255.0",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    )
                                                                                                                ],
                                                                                                                alignment=flet.MainAxisAlignment.START,
                                                                                                            ),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.CENTER,
                                                                                                            spacing= 40,
                                                                                                    ),
                                                                                                    flet.Row(
                                                                                                    [flet.FilledTonalButton("Настроить",
                                                                                                                                   icon=flet.Icons.SETTINGS,
                                                                                                                                   bgcolor= orange,
                                                                                                                                   color= "black",
                                                                                                                                   on_click=lambda e: print("k"),
                                                                                                                                   icon_color="black"),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.END,
                                                                                                    ),
                                                                                                ],
                                                                                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                                                                alignment=flet.MainAxisAlignment.CENTER,
                                                                                                spacing= 20
                                                                                            ),
                                                                                            width=282,
                                                                                            height=161,
                                                                                            padding=10,
                                                                                            bgcolor=white,
                                                                                            border_radius=20,
                                                                                        ),
                                                                                        color=white,
                                                                                        shadow_color="black",
                                                                                    )],
                                                                                    spacing= 5,
                                                                                    horizontal_alignment=flet.CrossAxisAlignment.CENTER),
                                                                                    flet.Column(
                                                                                    [flet.Text(
                                                                                        value="Eth2",
                                                                                        color="black"),
                                                                                    flet.Card(
                                                                                        content=flet.Container(
                                                                                            content=flet.Column(
                                                                                                [flet.Row([
                                                                                                            flet.Column([
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv4)",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "mac адрес",
                                                                                                                    color= "black"
                                                                                                                ),
                                                                                                                flet.Text(
                                                                                                                    value= "IP-адрес(IPv6)",
                                                                                                                    color="black"
                                                                                                                )
                                                                                                            ],
                                                                                                            horizontal_alignment= flet.CrossAxisAlignment.START
                                                                                                            ),
                                                                                                            flet.Column(
                                                                                                                [
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="255.255.255.0",
                                                                                                                        color="black"
                                                                                                                    ),
                                                                                                                    flet.Text(
                                                                                                                        value="192.168.1.42",
                                                                                                                        color="black"
                                                                                                                    )
                                                                                                                ],
                                                                                                                alignment=flet.MainAxisAlignment.START,
                                                                                                            ),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.CENTER,
                                                                                                            spacing= 40,
                                                                                                    ),
                                                                                                    flet.Row(
                                                                                                    [flet.FilledTonalButton("Настроить",
                                                                                                                                   icon=flet.Icons.SETTINGS,
                                                                                                                                   bgcolor= orange,
                                                                                                                                   color= "black",
                                                                                                                                   icon_color="black",
                                                                                                                                   on_click=lambda e: print("k")),
                                                                                                            ],
                                                                                                            alignment=flet.MainAxisAlignment.END,
                                                                                                    ),
                                                                                                ],
                                                                                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                                                                alignment=flet.MainAxisAlignment.CENTER,
                                                                                                spacing= 20
                                                                                            ),
                                                                                            width=282,
                                                                                            height=161,
                                                                                            padding=10,
                                                                                            bgcolor=white,
                                                                                            border_radius=20,
                                                                                        ),
                                                                                        color=white,
                                                                                        shadow_color="black",
                                                                                    ),
                                                                                        ],
                                                                                    spacing= 5,
                                                                                    horizontal_alignment=flet.CrossAxisAlignment.CENTER),
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
                                                                    flet.Column(
                                                                        [flet.Text(value="Eth3",
                                                                               color="black"),
                                                                        flet.Card(
                                                                        content=flet.Container(
                                                                            content=flet.Column(
                                                                                [flet.Row([
                                                                                    flet.Column([
                                                                                        flet.Text(
                                                                                            value="IP-адрес(IPv4)",
                                                                                            color="black"
                                                                                        ),
                                                                                        flet.Text(
                                                                                            value="mac адрес",
                                                                                            color="black"
                                                                                        ),
                                                                                        flet.Text(
                                                                                            value="IP-адрес(IPv6)",
                                                                                            color="black"
                                                                                        )
                                                                                    ],
                                                                                    horizontal_alignment=flet.CrossAxisAlignment.START
                                                                                    ),
                                                                                    flet.Column(
                                                                                    [
                                                                                        flet.Text(
                                                                                            value="192.168.1.42",
                                                                                            color="black"
                                                                                        ),
                                                                                        flet.Text(
                                                                                            value="255.255.255.0",
                                                                                            color="black"
                                                                                        ),
                                                                                        flet.Text(
                                                                                            value="192.168.1.42",
                                                                                            color="black"
                                                                                        )
                                                                                    ],
                                                                                    alignment=flet.MainAxisAlignment.START,
                                                                                ),
                                                                            ],
                                                                                alignment=flet.MainAxisAlignment.CENTER,
                                                                                spacing=40,
                                                                            ),
                                                                                flet.Row(
                                                                                    [flet.FilledTonalButton(
                                                                                        "Настроить",
                                                                                        icon=flet.Icons.SETTINGS,
                                                                                        bgcolor=orange,
                                                                                        color="black",
                                                                                        icon_color="black",
                                                                                        on_click=lambda e: print("k")),
                                                                                     ],
                                                                                    alignment=flet.MainAxisAlignment.END,
                                                                                ),
                                                                            ],
                                                                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                                            alignment=flet.MainAxisAlignment.CENTER,
                                                                            spacing=20
                                                                        ),
                                                                        width=282,
                                                                        height=161,
                                                                        padding=10,
                                                                        bgcolor=white,
                                                                        border_radius=20,
                                                                    ),
                                                                    color=white,
                                                                    shadow_color="black",
                                                                ),
                                                                         ],
                                                                    spacing= 5,
                                                                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                                                    alignment= flet.MainAxisAlignment.CENTER),
                                                            ]
                                          ),
                           )
                           # flet.Image(
                           #           src="Assets/GMB.png",
                           #           width=343,
                           #           height=558,
                           #           fit=flet.ImageFit.CONTAIN,
                           #
                           #   )
                           # flet.Container(bgcolor=white, width = 1370, height= 490, border_radius= 30)
                          ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                alignment=flet.MainAxisAlignment.CENTER,
                spacing=20,
                ))