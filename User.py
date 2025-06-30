import hashlib
import os

admin_login = ""

def init_file():  # Инициализация файла, если этого не сделать программа вылетит c ошибкой, что файла нет
    """Создает файл пользователей"""
    if not os.path.exists('assets/Users.txt'):
        with open('assets/Users.txt', 'w'):
            pass


def add_user(login: str, password: str) -> bool:
    """Добавляет пользователя в файл"""
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

    for user in users:
        args = user.split(':')
        if login == args[0]:  # Если логин уже есть, пароль не проверяем, шанс взлома увеличится(кто-то мб узнает пароль)
            return False  # Тут можно написать что угодно, будь то HTML статус(409 - conflict), либо просто фразу ошибки

    with open('assets/Users.txt', 'a') as f:
        f.write(f'{login}:{password}\n')  # Добавляем нового пользователя
    return True


def get_user(login, password):
    """Проверяет логин и пароль пользователя"""
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

    for user in users:
        args = user.split(':')
        if login == args[0] and password == args[1]:  # Если пользователь с таким логином и паролем существует
            return True
    return False

def get_user_login(login):
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

    for user in users:
        args = user.split(':')
        if login == args[0]:  # Если пользователь с таким логином и паролем существует
            return True
    return False

def get_users():
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла
    # for user in users:
    #     args = user.split(':')
    #     login = args[0]
    return users

def change_password(login, password):
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

        with open('assets/Users.txt', 'w') as fw:
            for user in users:
                args = user.split(':')
                if login != args[0]:
                    fw.write(f'{args[0]}:{args[1]}\n')

    with open('assets/Users.txt', 'a') as f:
        f.write(f'{login}:{hashlib.sha256(password.encode()).hexdigest()}\n')  # Добавляем нового пользователя

    print("Deleted")

    return True

def delete_user(login):
    with open('assets/Users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

        with open('assets/Users.txt', 'w') as fw:
            for user in users:
                args = user.split(':')
                if login != args[0]:
                    fw.write(f'{args[0]}:{args[1]}\n')

