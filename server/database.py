import psycopg2
from psycopg2.extras import DictCursor
import server

import utils


DB_CONNECTION_STRING = utils.get_db_connection_string()


def add_user(steamid:str, name: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profiles (steamid, name) SELECT '{steamid}', '{name}' WHERE NOT EXISTS(SELECT * FROM profiles WHERE steamid=('{steamid}'));")
        print(f"added user {name} with steamid {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def get_users():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM profiles;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def add_item(name: str, type: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""INSERT INTO items (name, "type") SELECT '{name}', '{type}' WHERE NOT EXISTS(SELECT * FROM items WHERE name=('{name}'));""")
        print(f"added item {name} with type {type}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_item_price(item_name: str, price: int, date: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', '{price}', '{date}';")
        print(f"added price {price} to item {item_name}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_to_inventory(steamid: str, item_name: str, quantity: int):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profile_items (profile, item, quantity) VALUES ('{steamid}', '{item_name}','{quantity}');")
        print(f"added item {item_name} to inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def set_inventory(steamid: str, inventory: dict):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"DELETE FROM profile_items WHERE profile = '{steamid}';")
        for item_name in inventory:
            add_item(inventory[item_name]["name"], inventory[item_name]["type"])
            add_to_inventory(steamid, inventory[item_name]["name"], inventory[item_name]["quantity"])
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def get_inventory(steamid: str):
    '''[profile, item_name, quantity, price, type, date]'''
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"SELECT profile, profile_items.item, quantity, price, type, date FROM profile_items JOIN items on item = items.name join item_price on profile_items.item=item_price.item WHERE profile = '{steamid}' order by date;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def get_item_list():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"SELECT * FROM items;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def get_latest_prices():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        querry = """
            SELECT ip.item, ip.date, ip.price
            FROM item_prices ip
            JOIN (
            SELECT item, MAX(date) AS max_date
            FROM item_prices
            GROUP BY item
            ) latest ON ip.item = latest.item AND ip.date = latest.max_date;
            """
        # cursor.execute(f"SELECT item_prices.item, price, quantity FROM item_prices JOIN profile_items on profile_items.item = item_prices.item;")
        cursor.execute(querry)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

