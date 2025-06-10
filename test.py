import flet as ft


def main(page: ft.Page):
    page.title = "Простое приложение"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def button_click(e):
        page.add(ft.Text("Кнопка нажата!"))

    page.add(
        ft.Text("Привет, Flet!", size=30),
        ft.ElevatedButton("Нажми меня", on_click=button_click)
    )


ft.app(target=main)