import flet
import User
from User import change_password, get_user_login


def main(page: flet.Page):


    def handle_profile_button(x):
        def change_password(e):
            login = dialog_field.controls[0].value
            new_password = dialog_field.controls[1].value
            repeat_password = dialog_field.controls[2].value

            if get_user_login(login): # if login is correct(user exists)
                if new_password == repeat_password:
                    User.change_password(login, new_password)
                    print("successfully change password")
                else:
                    dialog_field.controls[1].value = ""
                    dialog_field.controls[2].value = ""
                    dialog_field.controls[1].error_text = "Пароли не совпадают"
                    dialog_field.controls[2].error_text = "Пароли не совпадают"
                    page.update()
                    return
            else:
                dialog_field.controls[0].error_text = "Пользователя с таким логином не существует"
                dialog_field.controls[1].value = ""
                dialog_field.controls[2].value = ""
                page.update()
                return

            page.close(dialog)
            page.update()

        def on_click(e):
            print('a')
            dialog_field.controls[0].error_text = None
            dialog_field.controls[1].error_text = None
            dialog_field.controls[2].error_text = None
            page.update()

        dialog_field = (
            flet.Column(
                [flet.TextField(bgcolor="white", label="Имя пользователя:", width=350, color="black", selection_color="orange",
                                focused_border_color="orange", cursor_color="orange", border_radius=14, on_click = on_click),
                 flet.TextField(bgcolor="white", label="Новый пароль:", width=350, color="black", selection_color="orange",
                                focused_border_color="orange", cursor_color="orange", border_radius=14, on_click = on_click),
                 flet.TextField(bgcolor="white", label="Повторите пароль:", width=350, color="black", selection_color="orange",
                                focused_border_color="orange", cursor_color="orange", border_radius=14, on_click = on_click),
                 flet.ElevatedButton(text="Сохранить", color="black", bgcolor="orange", on_click=change_password)
                 ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                alignment=flet.MainAxisAlignment.CENTER,
                spacing=40

            ))

        dialog = flet.AlertDialog(
            content=flet.Container(
                width = 400,
                height = 350,
                content=dialog_field
            ),
            bgcolor="white",
            on_dismiss=lambda e: print("Dialog dismissed!"),
            content_padding=50,
        )

        page.open(dialog)
        dialog.open = True
        page.update()

    page.add(flet.ElevatedButton(text="press", on_click=handle_profile_button))

flet.app(target=main, view=flet.WEB_BROWSER, assets_dir="../assets")


