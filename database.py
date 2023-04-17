import psycopg2
from psycopg2.extras import DictCursor

import utils


def add_user(steamid:str, name: str):
    try:
        dbConn = psycopg2.connect(utils.utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profiles (steamid, name) SELECT '{steamid}', '{name}' WHERE NOT EXISTS(SELECT * FROM profiles WHERE steamid=('{steamid}'));")
        print(f"added user {name} with steamid {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def get_users():
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM profiles;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def add_item(name: str, type: str):
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""INSERT INTO items (name, type) SELECT '{name}', '{type}' WHERE NOT EXISTS(SELECT * FROM items WHERE name=('{name}'));""")
        print(f"added item {name} with type {type}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_item_price(item_name: str, price: int, date: str):
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', '{price}', '{date}';")
        print(f"added price {price} to item {item_name}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_to_inventory(steamid: str, item_name: str, quantity: int):
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profile_items (profile, item, quantity) VALUES ('{steamid}', '{item_name}','{quantity}');")
        print(f"added item {item_name} to inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def set_inventory(steamid: str, inventory: dict):
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        clear_inventory(steamid)
        for item_name in inventory:
            add_item(item_name, inventory[item_name]["type"])
            add_to_inventory(steamid, item_name, inventory[item_name]["quantity"])
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def clear_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"DELETE FROM profile_items WHERE profile = '{steamid}';")
        print(f"cleared inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def get_inventory(steamid: str):
    '''[profile, item_name, quantity, price, type, date]'''
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        querry = f"""
            SELECT ip.item, quantity, price
            FROM item_prices ip
            JOIN (
            SELECT item, MAX(date) AS max_date
            FROM item_prices
            GROUP BY item
            ) latest ON ip.item = latest.item AND ip.date = latest.max_date
            JOIN profile_items ON profile_items.item = ip.item
            WHERE profile = '{steamid}';
            """
        # cursor.execute(f"SELECT profile, profile_items.item, quantity, price, type, date FROM profile_items JOIN items on item = items.name join item_price on profile_items.item=item_price.item WHERE profile = '{steamid}' order by date;")
        cursor.execute(querry)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def get_item_list():
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""
        SELECT items.name, sum(profile_items.quantity) as qnts FROM items
        JOIN profile_items ON profile_items.item = items.name
        GROUP BY items.name
        order by qnts desc
        ;
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def get_latest_prices():
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""
            SELECT price, sum(profile_items.quantity) AS qnts, this.item FROM profile_items
            JOIN (
                SELECT ip.item, ip.date, ip.price
                FROM item_prices ip
                JOIN (
                SELECT item, MAX(date) AS max_date
                FROM item_prices
                GROUP BY item
                ) latest ON ip.item = latest.item AND ip.date = latest.max_date
                ORDER BY price DESC
            ) this ON this.item = profile_items.item
            GROUP BY this.item, price
            ORDER BY qnts DESC
            ;
            """)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()


def display():
    try:
        dbConn = psycopg2.connect(utils.DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            SELECT profiles.name, profile_items.item, profile_items.quantity, item_prices.date, item_prices.price FROM profiles
            JOIN profile_items ON profiles.steamid = profile_items.profile
            JOIN item_prices ON profile_items.item = item_prices.item
            ORDER BY item_prices.date DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()


