#import telebot
#from telebot import types
from aiogram import *
import sqlite3
import asyncio
from sqlite3 import Error

#СКьюЛь часть
PATH = "main.db"

CREATE_DATABASE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  class TEXT NOT NULL,
  login TEXT NOT NULL,
  password TEXT NOT NULL,
  balance INTEGER NOT NULL
);
"""

DROP_DATABASE_QUERY = """
DROP TABLE users;
"""

def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Query executed successfully -", query.replace("\n", " "))
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def INIT(conn):
    execute_query(conn, CREATE_DATABASE_QUERY)
    
def DROP_ALL(conn):
    execute_query(conn, DROP_DATABASE_QUERY)

def RECREATE(conn):
    DROP_ALL(conn)
    INIT(conn)
def SELECT_USERS(conn):
    return execute_read_query(conn, "SELECT * FROM users")
def reg(_name, _surname, _class, _login, _password):
    query = f"""INSERT INTO users(name, surname, class, login, password, balance) VALUES ('{_name}', '{_surname}', '{_class}', '{_login}', '{_password}', 0);
"""
    print(query)
    execute_query(conn, query)
conn = create_connection(PATH)

#СКьюЛь часть энд
#Важные переменные декларэйшн
bot = Bot('5860281367:AAGmZCTEvrJRXPLOV8bXGtf4JMlwNKir_YU')
dp = Dispatcher(bot)
USERS = []
LOGIN = {}
#Важные переменные деклерейшн энд

async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Добро пожаловать в НикольКредитБанк!')
#bot.polling(non_stop = True)

async def register(message):
    global USERS
    try:
        _name, _surname, _class, _login, _password = message.get_args().split()
    except ValueError:
        await message.answer("""Пожалуйста, введите свое имя, фамилию, класс, логин и пароль, который вы себе поставите, например:
/reg Петров Иван 7Б petrov qwerty
                             """)
    else:
        USERS = SELECT_USERS(conn)
        print(USERS, _login)
        for el in USERS:
            if el[-3] == _login:
                await message.answer("Этот логин уже занят!")
                return 0
        reg(_name, _surname, _class, _login, _password)
        await message.answer("Регистрация проведена успешно!")
    USERS = SELECT_USERS(conn)

async def login(message):
    try:
        _login, _password = message.get_args().split()
    except ValueError:
        await message.answer("""Пожалуйста, введите после команды через пробел логин и пароль, например:
/login admin 228pass
""")
    else:
        for el in USERS:
            if el[-3] == _login:
                break
        else:
            await message.answer("Такого пользователя не существует!")
            return 0
        if _password == el[-2]:
            await message.answer("Вход успешен!")
            LOGIN[message.chat.id] = _login
        else:
            await message.answer("Пароль неверный!")
    print(LOGIN)

async def unlogin(message):
    try:
        LOGIN.pop(message.chat.id)
        print(LOGIN)
        await message.answer("Вы успешно вышли из аккаунта!")
    except:
        await message.answer("Вы не входили в аккаунт!")

async def main():
    global USERS
    INIT(conn)
    USERS = SELECT_USERS(conn)
    print(USERS)
    #reg("Тимофей", "Блинов", 8, "Д", "123")
    dp.register_message_handler(start, commands = ['start'])
    dp.register_message_handler(register, commands = ['reg'])
    dp.register_message_handler(login, commands = ["login"])
    dp.register_message_handler(unlogin, commands = ["unlogin"])
    await dp.start_polling(bot)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    conn = 0
