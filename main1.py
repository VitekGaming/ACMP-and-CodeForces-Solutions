#import telebot
#from telebot import types
from aiogram import *
import sqlite3
import asyncio
from sqlite3 import Error

#СКьюЛ часть
PATH = "PATH TO DATABASE.db"

CREATE_DATABASE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
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

def execute_read_query(connection, query):
    cursor = connection.cursor()
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

conn = create_connection(PATH)

#СКьюЛ часть энд

bot = Bot('5860281367:AAGmZCTEvrJRXPLOV8bXGtf4JMlwNKir_YU')
dp = Dispatcher(bot)

async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Добро пожаловать в НикольКредитБанк!')
#bot.polling(non_stop = True)


async def main():
    dp.register_message_handler(start, commands = ['start'])
    await dp.start_polling(bot)
asyncio.run(main())
