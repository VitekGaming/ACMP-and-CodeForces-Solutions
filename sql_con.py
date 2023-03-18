import sqlite3
from sqlite3 import Error

# СКьюЛь часть
PATH = "main.db"

CREATE_DATABASE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  class TEXT NOT NULL,
  login TEXT NOT NULL,
  password TEXT NOT NULL,
  balance INTEGER NOT NULL,
  privilege INTEGER DEFAULT(1)
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


conn = create_connection(PATH)
last = ""
while True:
    com = input(">>> ")
    line = False
    if com == "INIT":
        INIT(conn)
        continue
    elif com == "DROP_ALL":
        DROP_ALL(conn)
        continue
    elif com == "RECREATE":
        RECREATE(conn)
        continue
    elif com == "!last":
        com = last
    if len(com) > 1 and com[0] == "!":
        line = True
        last = com
        com = com[1:]
    else:
        last = com
    res = execute_read_query(conn, com)
    if res != None:
        if line:
            try:
                for el in res:
                    print(el)
            except:
                pass
        else:
            print(res)