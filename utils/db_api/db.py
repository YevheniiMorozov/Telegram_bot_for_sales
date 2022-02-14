import sqlite3 as sq
from loader import bot


def sql_start():
    global base, cur
    base = sq.connect("tut_bd.db")
    cur = base.cursor()
    if base:
        print("db connected")
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT PRIMARY KEY, category TEXT, name TEXT, description TEXT, price TEXT)")


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sql_read(category):
    return cur.execute("SELECT * FROM menu WHERE category = ?", (category, )).fetchall()

# async def sql_read(message, category):
#     for ret in cur.execute("SELECT * FROM menu WHERE category = ?", (category, )).fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[2]}\nОпис: {ret[3]}\nЦіна: {ret[4]}')


async def sql_read_admin():
    return cur.execute("SELECT * FROM menu").fetchall()


async def sql_del_command(data):
    cur.execute("DELETE FROM menu WHERE name = ?", (data, )).fetchall()
    base.commit()
