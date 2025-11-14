
import subprocess


import flet

from charts import BarChart, Curve
# from main import DEFAULT_FLET_PORT

grey = "#565759"
white = "#EAEAEA"
orange = "#F7941E"
green = "#59A343"

class InfoView:
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.local_ip = self.app.user_ip
        self.temperature = self.get_temperature()
        self.date = "24.10.2025"
        self.time = "13:33:33"
        self.work_time = "0 дней 15 ч 37 мин"
        self.RAM = "184 МиБ/\n1,92 ГиБ"
        self.ROM = "184 МиБ/\n1,92 ГиБ"
        self.run_out = 0.0
        self.battery_voltage = 3000
        # self.bar = BarChart(self.battery, self.page)
        # self.battery_chart = self.bar.chart
        self.battery_chart = BarChart(self.battery_voltage).chart
        self.RAM_perc = 95
        self.RAM_chart = Curve(orange, self.RAM_perc).chart
        self.ROM_perc = 43
        self.ROM_chart = Curve("#8BBAE0", self.ROM_perc).chart
        self.cpu = {"1 мин" : 0.37, "5 мин" : 0.26, "15 мин" : 0.25}

        # self.ip = ""
        # asyncio.run(self.monitor_ips())

        self.upper_row = (
            flet.Container(
                flet.Row(
                    controls=[flet.Column(
                        [flet.Text(self.local_ip, size=23, weight=flet.FontWeight.W_600, color="#333333"),
                                flet.Text("Текущее устройство", size=15, color="black")],
                                spacing=0,
                            ),
                            flet.Row([
                                 flet.Row(
                                     [flet.Stack([
                                        flet.Container(content=flet.CircleAvatar(bgcolor="#D9D9D9", radius=26),
                                                       alignment=flet.alignment.center,),
                                        flet.Icon(flet.Icons.THERMOSTAT_ROUNDED, color="#333333", size=28)
                                    ], alignment=flet.alignment.center),
                                     flet.Column([flet.Text(self.temperature, size=23, weight=flet.FontWeight.W_600, color="#333333"),
                                                  flet.Text("Температура", size=15, color="black")],
                                                 spacing=0),
                                 ], vertical_alignment=flet.CrossAxisAlignment.END),
                                 flet.Row([
                                     flet.Stack([
                                         flet.Container(content=flet.CircleAvatar(bgcolor="#D9D9D9", radius=26),
                                                       alignment=flet.alignment.center, ),
                                         flet.Icon(flet.Icons.CALENDAR_MONTH_ROUNDED, color="#333333", size=23)
                                     ], alignment=flet.alignment.center),
                                     flet.Column([
                                         flet.Text(f"{self.date}\n{self.time}", size=23, weight=flet.FontWeight.W_600, color="#333333"),
                                         flet.Text("Дата и время", size=15, color="black")
                                     ],spacing=0),
                                ],
                                 vertical_alignment=flet.CrossAxisAlignment.END),
                            ], vertical_alignment=flet.CrossAxisAlignment.END, spacing=82),

                            flet.IconButton(icon=flet.Icons.REFRESH_ROUNDED, style=flet.ButtonStyle(color=orange), icon_size=25)
                    ],
                    vertical_alignment=flet.CrossAxisAlignment.END, alignment=flet.MainAxisAlignment.CENTER,spacing=279
                ),
            )
        )

        self.info_containers=(
            flet.Row([
                flet.Column([
                    flet.Row([
                        flet.Container(
                            flet.Row([
                                flet.Stack([
                                    flet.Container(content=flet.CircleAvatar(bgcolor=white, radius=34),
                                                   alignment=flet.alignment.center, ),
                                    flet.Icon(flet.Icons.HOME_ROUNDED, color="#333333", size=38)
                                ], alignment=flet.alignment.center),
                                flet.Column([
                                    flet.Text("Имя хоста", color=orange, size=15),
                                    flet.Text("sa.local", color="#333333", size=21, weight=flet.FontWeight.W_600)
                                ], alignment=flet.MainAxisAlignment.CENTER
                                )
                            ],vertical_alignment=flet.CrossAxisAlignment.CENTER, spacing=40),
                        # padding=flet.padding.Padding(24, 8, 16, 24),
                        bgcolor="#D9D9D9", width=436, height=86,border_radius=43,
                        shadow=flet.BoxShadow(color="#C8C8C8",
                                              offset=flet.Offset(1, 3),
                                              blur_radius=2,
                                              spread_radius=1
                                              ),
                        animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                        scale=flet.Scale(scale=1),
                        on_hover=self.animate,
                        padding=flet.padding.Padding(24, 0,0,0)
                        ),
                        flet.Container(content=flet.Image("favicon.png", width=124, height=81),width=304,height=84,
                                       animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                                       scale=flet.Scale(scale=1),
                                       on_hover=self.animate
                                       )
                        # flet.Container(bgcolor="#D9D9D9",width=308,height=94,border_radius=35)
                    ], spacing=15,vertical_alignment=flet.CrossAxisAlignment.CENTER),
                    flet.Row([
                        flet.Container(
                            flet.Row([
                                flet.Stack([
                                    flet.Container(content=flet.CircleAvatar(bgcolor=white, radius=34),
                                                   alignment=flet.alignment.center, ),
                                    flet.Icon(flet.Icons.NUMBERS_ROUNDED, color="#333333", size=38)
                                ], alignment=flet.alignment.center),
                                flet.Column([
                                    flet.Text("Серийный номер", color=orange, size=15),
                                    flet.Text("123456-78", color="#333333", size=21, weight=flet.FontWeight.W_600)
                                ],alignment=flet.MainAxisAlignment.CENTER)
                            ], vertical_alignment=flet.CrossAxisAlignment.CENTER, spacing=40),
                            padding=flet.padding.Padding(24, 0, 0, 0),
                            bgcolor="#D9D9D9",width=436, height=86,border_radius=43,
                            shadow=flet.BoxShadow(color="#C8C8C8",
                                                 offset=flet.Offset(1, 3),
                                                 blur_radius=2,
                                                 spread_radius=1
                                                 ),
                            animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                            scale = flet.Scale(scale=1),
                            on_hover = self.animate
                        ),
                        flet.Container(
                            flet.Column([
                                flet.Text("Время работы", color="black", size=18),
                                flet.Text(self.work_time, color="#333333", size=21, weight=flet.FontWeight.W_600)
                            ]),
                            bgcolor="#D9D9D9",width=304,height=94,border_radius=35,
                            padding=flet.padding.Padding(29,17,16,15),
                            shadow=flet.BoxShadow(color="#C8C8C8",
                                                 offset=flet.Offset(1, 3),
                                                 blur_radius=2,
                                                 spread_radius=1
                                                 ),
                            animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                            scale=flet.Scale(scale=1),
                            on_hover=self.animate
                       )
                    ],spacing=15,vertical_alignment=flet.CrossAxisAlignment.CENTER),
                    flet.Row([
                        self.port_info("eth0", 1000, 82392467, 42.1, 1086867, 150934),
                        self.port_info("eth1", 100, 0,0,0,0)
                    ], spacing=15),
                    flet.Row([
                        self.port_info("eth2", 100, 0,0, 0,0),
                        self.port_info("ecat", 100, 0,0,0,0)
                    ],spacing=15),
                    flet.Row([
                        flet.Container(
                            flet.Column([
                                flet.Text("Напряжение батареи часов", color="#333333", size=18),
                                self.battery_chart
                            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                            padding=flet.padding.Padding(29, 17, 16, 19),
                            bgcolor="#D9D9D9",width=570,height=107,border_radius=35,
                            shadow=flet.BoxShadow(color="#C8C8C8",
                                                offset=flet.Offset(1, 3),
                                                blur_radius=2,
                                                spread_radius=1
                                                ),
                            animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                            scale=flet.Scale(scale=1),
                            on_hover=self.animate
                        ),
                        flet.Container(
                            flet.Column([
                                flet.Text("Износ ПЗУ", color="black", size=18),
                                flet.Text(f"{str(self.run_out)} %", color="red" if self.run_out > 70.0 else green,
                                          weight=flet.FontWeight.W_600, size=21)
                            ], horizontal_alignment=flet.CrossAxisAlignment.START, alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                            padding=flet.padding.Padding(29, 17, 14, 15),
                            bgcolor="#D9D9D9",width=170,height=107,border_radius=35,
                            shadow=flet.BoxShadow(color="#C8C8C8",
                                                offset=flet.Offset(1, 3),
                                                blur_radius=2,
                                                spread_radius=1
                                                ),
                            animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                            scale=flet.Scale(scale=1),
                            on_hover=self.animate,
                            expand=True
                        )
                    ],spacing=15)
                ],spacing=15,alignment=flet.MainAxisAlignment.START),
                flet.Column([
                    flet.Container(
                        flet.Column([
                            flet.Text("Средняя загрузка процессора", color="black", size=18),
                            self._cpu()
                        ],alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor="#D9D9D9",width=436,height=194,border_radius=35,
                        padding=flet.padding.Padding(18, 17, 16, 15),
                        shadow=flet.BoxShadow(color="#C8C8C8",
                                            offset=flet.Offset(1, 3),
                                            blur_radius=2,
                                            spread_radius=1
                                            ),
                        animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                        scale=flet.Scale(scale=1),
                        on_hover=self.animate
                    ),
                    flet.Container(
                        flet.Row([
                            flet.Column([
                                flet.Text("ОЗУ", color="black", size=18),
                                flet.Text(self.RAM,color="#333333", size=21, weight=flet.FontWeight.W_600)
                            ],alignment=flet.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                            flet.Stack([
                                self.RAM_chart,
                                flet.Text(f"{self.RAM_perc} %", color="#333333", size=21, weight=flet.FontWeight.W_600, left=80)
                            ], alignment=flet.alignment.bottom_center)
                        ],  vertical_alignment=flet.CrossAxisAlignment.END,
                            alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                        bgcolor="#D9D9D9",width=436,height=207,border_radius=35,
                        padding=flet.padding.Padding(29, 17, 16, 15),
                        shadow=flet.BoxShadow(color="#C8C8C8",
                                              offset=flet.Offset(1, 3),
                                              blur_radius=2,
                                              spread_radius=1
                                              ),
                        animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                        scale=flet.Scale(scale=1),
                        on_hover=self.animate
                        ),
                    flet.Container(
                        flet.Row([
                            flet.Column([
                                flet.Text("ПЗУ", color="black", size=18),
                                flet.Text(self.ROM, color="#333333", size=21, weight=flet.FontWeight.W_600)
                            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                            flet.Stack([
                                self.ROM_chart,
                                flet.Text(f"{self.ROM_perc} %", color="#333333", size=21, weight=flet.FontWeight.W_600,
                                          left=80)
                            ], alignment=flet.alignment.bottom_center)
                        ], vertical_alignment=flet.CrossAxisAlignment.END,
                            alignment=flet.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                        bgcolor="#D9D9D9",width=436,height=207,border_radius=35,
                        padding=flet.padding.Padding(29, 17, 16, 15),
                        shadow=flet.BoxShadow(color="#C8C8C8",
                                             offset=flet.Offset(1, 3),
                                             blur_radius=2,
                                             spread_radius=1
                                             ),
                        animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                        scale=flet.Scale(scale=1),
                        on_hover=self.animate
                    )
                ],spacing=15)
            ],spacing=15, alignment=flet.MainAxisAlignment.CENTER)
        )

        self.layout = (
            flet.Container(
                flet.Column(
            [flet.Text("Системная информация", text_align=flet.alignment.center, color=orange, size=20),
                    flet.Column([
                        self.upper_row,
                        self.info_containers
                    ],spacing=51, horizontal_alignment=flet.CrossAxisAlignment.CENTER),
                    ],
                    spacing=51,alignment=flet.MainAxisAlignment.START, horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                ),expand=True, padding=20
            )
        )

    def _cpu(self):
        row = flet.Row(spacing=8)
        for minute, cpu in self.cpu.items():
            row.controls.append (
                flet.Container(
                    flet.Column([
                        flet.Text(minute, color=orange, size=15),
                        flet.Text(str(cpu), color="#333333", size=21, weight=flet.FontWeight.W_600)
                    ],alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=white,
                    width=129, height=101.53, border_radius=17,
                    padding=flet.padding.Padding(16,18,38,15),
                    animate_scale=flet.Animation(200, flet.AnimationCurve.LINEAR),
                    scale=flet.Scale(scale=1),
                    on_hover=self.animate
                )
            )

        return row

    def port_info(self, name, speed, rx, tx, pack_rx, pack_tx):
        if 1024 < rx <= 2**20:
            rx_union = "Kб"
            rx /= 1024
            rx = str(round(rx, 2))
        elif rx > 2**20:
            rx_union = "Mб"
            rx = rx/1024/1024
            rx = str(round(rx, 2))
        else:
            rx_union = "б"

        if 1024 < tx <= 2**20:
            tx_union = "Kб"
            tx /= 1024
            tx = str(round(tx, 2))
        elif tx > 2**20:
            tx_union = "Mб"
            tx = tx/1024/1024
            tx = str(round(tx, 2))
        else:
            tx_union = "б"

        if name == "eth0":
            up_down = self.app.eth0.get_up_down()
        elif name == "eth1":
            up_down  = self.app.eth1.get_up_down()
        elif name == "eth2":
            up_down = self.app.eth2.get_up_down()
        else:
            up_down = self.app.ecat.get_up_down()

        return flet.Container(
                    flet.Column([
                        flet.Row([
                            flet.Text(name, color=green if up_down else "#333333", size=20),
                            flet.Text(f"{str(speed)} Мбит/c", color="black", size=15)
                        ]),
                        flet.Row([
                            flet.Column([
                                # flet.Text(f"  {str(rx)} {rx_union}", color=green, size=21, weight=flet.FontWeight.W_600),
                                flet.Text("⬇ Получено", color="black", size=18, height=33),
                                flet.Text(f"{rx} {rx_union}", color=green, size=21, weight=flet.FontWeight.W_600),
                                flet.Text(f"{str(pack_rx)} пакетов", color="black", size=15)
                            ], width=130, spacing=0),
                            flet.Column([
                                # flet.Text(f"  {str(tx)} {tx_union}", color="red", size=21, weight=flet.FontWeight.W_600),
                                flet.Text("⬆ Отправлено", color="black", size=18, height=33),
                                flet.Text(f"{tx} {tx_union}", color="red", size=21, weight=flet.FontWeight.W_600),
                                flet.Text(f"{str(pack_tx)} пакетов", color="black", size=15)
                            ], spacing=0)
                        ], spacing=30)
                    ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor="#E6E6E6",width=370,height=146,border_radius=35,
                    padding=flet.padding.Padding(29,17,0,15),
                    shadow=flet.BoxShadow(color="#C8C8C8",
                                         offset=flet.Offset(1, 3),
                                         blur_radius=2,
                                         spread_radius=1
                                         ),
                    animate_scale=flet.Animation(300, flet.AnimationCurve.LINEAR),
                    scale=flet.Scale(scale=1),
                    on_hover=self.animate
                )

    def animate(self, e):
        if e.data == "true":
            e.control.scale = 1.03
        else:
            e.control.scale = 1
        self.page.update()

    def get_temperature(self):
        cmd = "vcgencmd measure_temp"
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

        temp = result.stdout.split("=")[1].strip()
        return temp


    # async def monitor_ips(self):
    #     connections = {} #{"ip": datetime}
    #
    #     async def get_connections(port: int):
    #         """Асинхронное получение активных подключений"""
    #         proc = await asyncio.create_subprocess_shell(
    #             f"sudo ss -tnp | grep ':{port} '",
    #             stdout=asyncio.subprocess.PIPE,
    #             stderr=asyncio.subprocess.PIPE
    #         )
    #         stdout, stderr = await proc.communicate()
    #         if stderr:
    #             return []
    #
    #         lines = stdout.decode().strip().splitlines()
    #         active_ips = []
    #         for line in lines:
    #             parts = line.split()
    #             if len(parts) >= 5:
    #                 remote_addr = parts[4]  # например "192.157.13.0:53245"
    #                 if ":" in remote_addr:
    #                     ip, _ = remote_addr.rsplit(":", 1)  # оставляем только IP
    #                     active_ips.append(ip)
    #         return active_ips
    #
    #     async def monitor_connections():
    #         """Асинхронный мониторинг только по IP"""
    #         while True:
    #             active_ips = await get_connections(self.app.DEFAULT_FLET_PORT)
    #
    #             # Добавляем новые IP
    #             for ip in active_ips:
    #                 if ip not in connections:
    #                     connections[ip] = datetime.now()
    #
    #             # Удаляем неактивные IP
    #             for ip in list(connections.keys()):
    #                 if ip not in active_ips:
    #                     del connections[ip]
    #
    #             # Очистка экрана
    #             os.system("clear")
    #
    #             # Вывод таблицы
    #             print("-" * 50)
    #             print(f"{'IP-адрес':30} {'Время подключения'}")
    #             print("-" * 50)
    #
    #             sorted_conns = sorted(connections.items(), key=lambda x: x[1], reverse=True)
    #             self.local_ip = next(iter(sorted_conns))
    #
    #             for ip, ts in sorted_conns:
    #                 print(f"{ip:30} {ts.strftime('%H:%M:%S')}")
    #
    #             await asyncio.sleep(2)
    #
    #     await monitor_connections()