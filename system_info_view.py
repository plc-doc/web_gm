import subprocess
import time
import re

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

        self.local_ip = self.app.local_ip
        self.temperature = self.get_temperature()
        self.date = "24.10.2025"
        self.time = "13:33:33"
        self.work_time = self.get_time_of_working()
        self.RAM = self.get_RAM()[0]
        self.ROM = self.get_ROM()[0]
        self.run_out = 0.0
        self.battery_voltage = 3000
        # self.bar = BarChart(self.battery, self.page)
        # self.battery_chart = self.bar.chart
        self.battery_chart = BarChart(self.battery_voltage).chart
        self.RAM_perc = self.get_RAM()[1]
        self.RAM_chart = Curve(orange, self.RAM_perc).chart
        self.ROM_perc = self.get_ROM()[1]
        self.ROM_chart = Curve("#8BBAE0",  self.ROM_perc).chart
        # self.cpu = {"1 мин" : 0.37, "5 мин" : 0.26, "15 мин" : 0.25}
        self.cpu = self.cpu_usage_per_core()

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
                                     flet.Column([flet.Text(self.get_temperature(), size=23, weight=flet.FontWeight.W_600, color="#333333"),
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
                            flet.Text("Нагрузка по ядрам", color="black", size=18),
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
                                flet.Column(
                                    [flet.Text("Используется:", color="black", size=15),
                                    flet.Text(self.RAM,color="#333333", size=21, weight=flet.FontWeight.W_600)],
                                )
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
                                flet.Text(self.get_ROM()[0], color="#333333", size=21, weight=flet.FontWeight.W_600)
                            ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                            flet.Stack([
                                self.ROM_chart,
                                flet.Text(f"{self.get_ROM()[1]} %", color="#333333", size=21, weight=flet.FontWeight.W_600,
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
        for core, cpu in self.cpu.items():
            row.controls.append (
                flet.Container(
                    flet.Column([
                        flet.Text(core, color=orange, size=15),
                        flet.Text(str(cpu) + " %", color="#333333", size=21, weight=flet.FontWeight.W_600)
                    ],alignment=flet.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=white,
                    width=91, height=91, border_radius=17,
                    padding=flet.padding.Padding(12,18,38,15),
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

    def get_ROM(self):
        result = subprocess.run(
            ["df", "-h", "--output=size,used", "/dev/mmcblk0p2"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        size, used = lines[1].split()  # строка 0 — заголовки

        self.ROM = f"{ru_unit(used)}/\n{ru_unit(size)}"
        self.ROM_perc = float(used[:-1]) / float(size[:-1]) * 100

        return self.ROM, self.ROM_perc

    def get_RAM(self):
        cmd = "free -h"
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()

        for line in lines:
            if line.startswith("Mem:"):
                parts = line.split()
                total = parts[1]  # 3.7Gi
                used = parts[2]  # 208Mi
                break

        self.RAM = f"{ru_unit(used)}/\n{ru_unit(total)}"
        self.RAM_perc = float(used[:-1]) / float(total[:-1]) * 100

        return self.RAM, self.RAM_perc

    def read_cpu_stats(self):
        stats = {}
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("cpu") and line[3].isdigit():  # cpu0, cpu1, ...
                    parts = line.split()
                    cpu = parts[0]
                    values = list(map(int, parts[1:]))

                    total = sum(values)
                    idle = values[3] + values[4]  # idle + iowait

                    stats[cpu] = (total, idle)
        return stats

    def cpu_usage_per_core(self, interval=1.0):
        before = self.read_cpu_stats()
        time.sleep(interval)
        after = self.read_cpu_stats()

        usage = {}
        for cpu in before:
            total_diff = after[cpu][0] - before[cpu][0]
            idle_diff = after[cpu][1] - before[cpu][1]

            if total_diff == 0:
                percent = 0.0
            else:
                percent = (1 - idle_diff / total_diff) * 100

            usage[cpu] = round(percent, 2)

        return usage

    def russian_plural(self, number, forms):
        if 11 <= (number % 100) <= 19:
            return forms[2]
        elif number % 10 == 1:
            return forms[0]
        elif 2 <= (number % 10) <= 4:
            return forms[1]
        else:
            return forms[2]

    def get_time_of_working(self):
        # получаем вывод uptime
        result = subprocess.run(["uptime"], capture_output=True, text=True)
        text = result.stdout.strip()

        # достаем часть после "up" и до ",  <число> user"
        match = re.search(r"up (.*?),\s+\d+ user", text)
        if not match:
            return "Не удалось распознать uptime"

        up_str = match.group(1).strip()

        days = hours = minutes = 0

        # проверяем разные форматы
        # 1) "X days, HH:MM"
        match1 = re.match(r"(\d+)\s+days?,\s+(\d+):(\d+)", up_str)
        if match1:
            days = int(match1.group(1))
            hours = int(match1.group(2))
            minutes = int(match1.group(3))
        else:
            # 2) "X days, Y min"
            match2 = re.match(r"(\d+)\s+days?,\s+(\d+)\s+min", up_str)
            if match2:
                days = int(match2.group(1))
                minutes = int(match2.group(2))
            else:
                # 3) "HH:MM"
                match3 = re.match(r"(\d+):(\d+)", up_str)
                if match3:
                    hours = int(match3.group(1))
                    minutes = int(match3.group(2))
                else:
                    # 4) "Y min"
                    match4 = re.match(r"(\d+)\s+min", up_str)
                    if match4:
                        minutes = int(match4.group(1))

        # склонение
        days_str = self.russian_plural(days, ("день", "дня", "дней"))
        hours_str = self.russian_plural(hours, ("час", "часа", "часов"))
        minutes_str = self.russian_plural(minutes, ("минута", "минуты", "минут"))

        return f"{days} {days_str} {hours} {hours_str} {minutes} {minutes_str}"

def ru_unit(value: str) -> str:
    units = {
        "T": "Тб",
        "G": "Гб",
        "M": "Мб",
        "K": "Кб",
        "B": "байт"
    }

    unit = value[-1]     # последний символ
    number = value[:-1]  # всё перед ним

    return number + units.get(unit, unit)