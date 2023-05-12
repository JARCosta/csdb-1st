import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import server
import os
import utils


DB_CONNECTION_STRING = utils.get_db_connection_string()

"""
    for each item in item_prices get latest price

    SELECT ip2.item, ip2.date, price as latest_price from item_prices ip2
    JOIN(
    SELECT item, MAX(date) as date FROM item_prices ip
    GROUP BY item
    ) ip ON ip.item = ip2.item AND ip.date = ip2.date
"""


def print_function_info(func):
    def wrapper(*args, **kwargs):
        filename = os.path.abspath(__file__)
        line_number = func.__code__.co_firstlineno + 1
        print(f"I am in {filename}:{line_number} in {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@print_function_info
def add_user(steamid:str, name: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"INSERT INTO profiles (steamid, name) SELECT '{steamid}', '{name}' WHERE NOT EXISTS(SELECT * FROM profiles WHERE steamid=('{steamid}'));")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

def add_user_string(steamid:str, name: str):
    return f"INSERT INTO profiles (steamid, name) SELECT '{steamid}', '{name}' WHERE NOT EXISTS(SELECT * FROM profiles WHERE steamid=('{steamid}'));"

@print_function_info
def add_users(users: dict):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        query = "START TRANSACTION;"
        for i in users:
            query += add_user_string(i['steamid'], i['name'])
        query += "COMMIT;"
        cursor.execute(query)
        # cursor.execute(f"INSERT INTO profiles (steamid, name) SELECT '{steamid}', '{name}' WHERE NOT EXISTS(SELECT * FROM profiles WHERE steamid=('{steamid}'));")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@print_function_info
def get_users():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM profiles;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

@print_function_info
def get_users_db():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("""SELECT profiles.name, profile, SUM(quantity) sum, COUNT(profile) as unique, SUM(quantity*latest_price) total FROM profile_items pi
            JOIN(

            SELECT ip2.item, price as latest_price from item_prices ip2
            JOIN(

            SELECT item, MAX(date) as date FROM item_prices ip
            GROUP BY item

            ) ip ON ip.item = ip2.item AND ip.date = ip2.date

            ) lp ON lp.item = pi.item
            JOIN profiles on profile = profiles.steamid
            GROUP BY profiles.name, profile
                    """)
        all = cursor.fetchall()
        # if(all == []):
        #     all = cursor.execute("""SELECT name, profile, SUM(quantity) as sum, COUNT(item) as unique FROM "public"."profile_items"
        #         JOIN profiles on profiles.steamid = profile
        #         GROUP BY profiles.name, profile_items.profile
        #         """)
            # temp = cursor.fetchall()
            # for i in temp:
            #     i.append(0)
            # return temp
        return all
    finally:
        cursor.close()
        dbConn.close()



@print_function_info
def get_inventory_price(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""SELECT SUM(price*quantity) FROM profile_items JOIN item_prices ON profile_items.item = item_prices.item WHERE profile = '{steamid}';""")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        dbConn.close()

@print_function_info
def get_inventory_size(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""SELECT SUM(quantity) FROM profile_items WHERE profile = '{steamid}';""")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        dbConn.close()

@print_function_info
def get_inventory_unique_items_size(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""SELECT COUNT(*) FROM profile_items WHERE profile = '{steamid}';""")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        dbConn.close()

def create_item_string(item_name: str, item_type: str):
    item_name = item_name.replace("&", "%26")
    item_name = item_name.replace("'", "%27")
    return f"""INSERT INTO items (name, type) SELECT '{item_name}', '{item_type}' WHERE NOT EXISTS(SELECT * FROM items WHERE name=('{item_name}'));"""

@print_function_info
def create_item(item_name: str, item_type: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        query = "START TRANSACTION;"
        query += create_item_string(item_name, item_type)
        query += set_item_price_string(item_name,'null', date='01-01-1970')
        query += "COMMIT;"
        cursor.execute(query)
        print(f"added item {item_name} with type {item_type}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@print_function_info
def get_items():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"""SELECT * FROM items;""")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def set_item_price_string(item_name: str, price: int, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    item_name = item_name.replace("&", "%26")
    item_name = item_name.replace("'", "%27")
    return f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', {price}, '{date}' WHERE NOT EXISTS(SELECT * FROM item_prices WHERE item='{item_name}' AND date='{date}');"

@print_function_info
def set_item_price(item_name: str, price: int, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(set_item_price_string(item_name, price, date))
        print(f"added price {price} to item {item_name}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


def add_to_inventory_string(steamid: str, item_name: str, quantity: int, auto: bool):
    item_name = item_name.replace("&", "%26")
    item_name = item_name.replace("'", "%27")
    return f"""
    INSERT INTO profile_items (profile, item, quantity, auto) SELECT '{steamid}', '{item_name}','{quantity}', '{auto}' WHERE NOT EXISTS(SELECT * FROM profile_items WHERE profile = '{steamid}' AND item = '{item_name}');
    UPDATE profile_items SET quantity = {quantity} WHERE profile = '{steamid}' AND item = '{item_name}';
    """

@print_function_info
def add_to_inventory(steamid: str, item_name: str, quantity: int, auto: bool):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        query = "START TRANSACTION;"
        query += add_to_inventory_string(steamid=steamid, item_name=item_name, quantity=quantity, auto=auto)
        query += "COMMIT;"

        cursor.execute(query=query)
        
        # set price as 0 if not set
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(f"INSERT INTO item_prices (item, price, date) SELECT '{item_name}', '0', '{date}' WHERE NOT EXISTS( SELECT * FROM item_prices WHERE item = '{item_name}' );")


        print(f"added item {item_name} to inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@print_function_info
def alter_item(steamid, item, quantity):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"UPDATE profile_items SET quantity = {quantity} WHERE profile = '{steamid}' AND item = '{item}';")
        print(f"altered item {item} in inventory of {steamid}")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@print_function_info
def get_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        query = f"""
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
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

@print_function_info
def set_inventory(steamid: str, inventory: dict):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        clear_auto_inventory(steamid)
        query = "START TRANSACTION;"
        for item_name in inventory:
            query += create_item_string(item_name, inventory[item_name]["type"])
            query += add_to_inventory_string(steamid, item_name, inventory[item_name]["quantity"], True)
            query += set_item_price_string(item_name,'null', date='01-01-1970')
        query += "COMMIT;"
        print(query)
        cursor.execute(query=query)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@print_function_info
def clear_auto_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"DELETE FROM profile_items WHERE profile = '{steamid}' AND auto = 'true';")
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@print_function_info
def get_items_to_update():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        # only the ones with no price yet
        cursor.execute("""SELECT pi.item, ip.price
            FROM profile_items pi
            JOIN (
                SELECT item, MAX(date) as max_date
                FROM item_prices
                GROUP BY item
            ) max_prices ON pi.item = max_prices.item
            JOIN item_prices ip ON pi.item = ip.item AND ip.date = max_prices.max_date
            ORDER BY price DESC NULLS FIRST

            """)
        all = cursor.fetchall()
        if(all == []):
            cursor.execute(f"""
            SELECT items.name, sum(profile_items.quantity) as qnts FROM items
            JOIN profile_items ON profile_items.item = items.name
            GROUP BY items.name
            order by qnts desc
            ;
            """)
            all = cursor.fetchall()
        return all
    finally:
        cursor.close()
        dbConn.close()

def latest_price_string():
    return """
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
    """
            # WHERE price != 0

@print_function_info
def get_latest_prices():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(latest_price_string())
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def profile_items_string():
    return """
        SELECT p.name as profile, pi.item, pi.quantity, ip.price, TO_CHAR(ip.date, 'DD-MM-YY') as date
        FROM profile_items pi
        JOIN profiles p ON pi.profile = p.steamid
        JOIN (
            SELECT item, MAX(date) as max_date
            FROM item_prices
            GROUP BY item
        ) max_prices ON pi.item = max_prices.item
        JOIN item_prices ip ON pi.item = ip.item AND ip.date = max_prices.max_date
        ORDER BY quantity * price DESC NULLS LAST, profile ASC
    """

@print_function_info
def profile_items():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute(profile_items_string())
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

@print_function_info
def delete_item(item_name: str):
    item_name = item_name.replace("&", "%26")
    item_name = item_name.replace("'", "%27")
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

