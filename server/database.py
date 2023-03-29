import psycopg2
from psycopg2.extras import DictCursor
import server

import utils


DB_CONNECTION_STRING = utils.get_db_connection_string()


def add_user(steamid:str, name: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profiles (steamid, name) VALUES ('{steamid}', '{name}');")
        print(f"added user {name} with steamid {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


def add_item(name: str, type: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO items (name, type) VALUES ('{name}', '{type}');")
        print(f"added item {name} with type {type}")
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

def add_item_price(item_name: str, price: int, date: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO item_prices (item, price) VALUES ('{item_name}', '{price}');")
        print(f"added price {price} to item {item_name}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()