import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
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

def create_item(item_name: str, item_type: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""INSERT INTO items (name, type) SELECT '{item_name}', '{item_type}' WHERE NOT EXISTS(SELECT * FROM items WHERE name=('{item_name}'));""")
        print(f"added item {item_name} with type {item_type}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def set_item_price(item_name: str, price: int):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', '{price}', '{date}';")
        print(f"added price {price} to item {item_name}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_to_inventory(steamid: str, item_name: str, quantity: int, auto: bool):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        #TODO: maybe store date of item addition
        cursor.execute(f"INSERT INTO profile_items (profile, item, quantity, auto) SELECT '{steamid}', '{item_name}','{quantity}', '{auto}' WHERE NOT EXISTS(SELECT * FROM profile_items WHERE profile = '{steamid}' AND item = '{item_name}');")
                                                # quantity = quantity + new quantity OR quantity = new quantity ?
        cursor.execute(f"UPDATE profile_items SET quantity = {quantity} WHERE profile = '{steamid}' AND item = '{item_name}';")
        
        # set price as 0 if not set
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', '0', '{date}' WHERE NOT EXISTS( SELECT * FROM item_prices WHERE item = '{item_name}' );")


        print(f"added item {item_name} to inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def get_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        querry = f"""
                SELECT ip.item, quantity, price, items.type
                FROM item_prices ip
                JOIN (
                SELECT item, MAX(date) AS max_date
                FROM item_prices
                GROUP BY item
                ) latest ON ip.item = latest.item AND ip.date = latest.max_date
                JOIN profile_items ON profile_items.item = ip.item
                JOIN items on ip.item = items.name
                WHERE profile = '{steamid}' AND quantity > 0 
        """
                # AND (
                #     items.type like '%Base Grade%' OR
                #     items.type like '%Sticker%' OR
                #     items.type like '%Qualidade%'
	            #     );
        cursor.execute(querry)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def set_inventory(steamid: str, inventory: dict):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        clear_auto_inventory(steamid)
        for item_name in inventory:
            create_item(item_name, inventory[item_name]["type"])
            add_to_inventory(steamid, item_name, inventory[item_name]["quantity"], True)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def clear_auto_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"DELETE FROM profile_items WHERE profile = '{steamid}' AND auto = 'true';")
        print(f"cleared inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


def get_item_list():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
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
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""
            SELECT price, sum(profile_items.quantity), this.item FROM profile_items
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
            ORDER BY price * sum(profile_items.quantity) DESC
            ;
            """)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def delete_item(item_name: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""
        DELETE FROM item_prices WHERE item = '{item_name}';
        DELETE FROM profile_items WHERE item = '{item_name}';
        DELETE from items WHERE name = '{item_name}';
        """)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

