

from datetime import datetime
import json
from alive_progress import alive_bar
from time import sleep

import requests
import database
from utils import HEADERS


users = [
    {"name": "Jar", "steamid":"76561198285623099"},
    {"name": "Navi", "steamid":"76561198185395854"},
    {"name": "Pulga", "steamid":"76561198201367491"},
    {"name": "Why", "steamid":"76561198200839393"},
]

def __init__():
    start = datetime.now()
    database.add_users(users)
    print(f"Query took {datetime.now() - start}")


def add_user(name: str, steamid: str):
    database.add_user(name, steamid)

def get_users():
    return database.get_users()

def get_users_db():
    return database.get_users_db()

def get_inventory_price(steamid: str):
    return database.get_inventory_price(steamid)

def get_inventory_size(steamid: str):
    return database.get_inventory_size(steamid)

def get_inventory_unique_items_size(steamid: str):
    return database.get_inventory_unique_items_size(steamid)

def get_items():
    return database.get_items()

def get_item_list():
    return [{"name":i[0]} for i in database.get_items_to_update()]
    return [{"name":i[0],"quantity":i[1]} for i in database.get_items_to_update()]



def set_inventory(steamid: str, inventory: dict):
    return database.set_inventory(steamid, inventory)

def add_item(steamid : str, item_name: str, item_type: str, quantity: int):
    database.create_item(item_name, item_type)
    database.add_to_inventory(steamid, item_name, quantity, False)

def alter_item(steamid, item, quantity):
    return database.alter_item(steamid, item, quantity)


        

def get_inventory(steamid: str):
    return [{"name":i[0].replace("%26", "&"),"quantity":i[1],"price":i[2], "type":i[3]} for i in database.get_inventory(steamid)]



def update_item_price(item_name: str):
    while True:
        try:
            price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_name}'
            response = requests.get(price_url, headers=HEADERS)
            price = float(json.loads(response.content)['lowest_price'][:-1].replace(",",".").strip("-"))
            break
        except (TypeError,KeyError) as e:
            # if(e == "lowest_price"):
            print(price_url)
            print(e, "at", item_name)
            with alive_bar(600) as bar:
                for _ in range(600):
                    sleep(0.1)
                    bar()
    database.set_item_price(item_name, price)

def get_latest_prices():
    data =[{"name":i[2].replace("%26", "&"),"quantity":i[1],"price":i[0], "total price":round(float(i[1] or 0)*float(i[0] or 0),2)} for i in database.get_latest_prices()]
    
    total_items = 0
    total_price = 0
    for i in data:
        total_items += i["quantity"]
        total_price += i["total price"]
    if total_items > 0:
        average_price = total_price/total_items
    else:
        average_price = 0
    
    total = [{"name":"Total","quantity":total_items,"price":round(average_price,2),"total price":round(total_price,2)}]

    return [total, data]


def profile_items():
    return database.profile_items()


