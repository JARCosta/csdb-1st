

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
]

def __init__():
    for i in users:
        database.add_user(i["steamid"], i["name"])


def add_user(name: str, steamid: str):
    database.add_user(name, steamid)

def get_users():
    return database.get_users()



def get_item_list():
    return [{"name":i[0],"type":i[1]} for i in database.get_item_list()]



def set_inventory(steamid: str, inventory: dict):
    return database.set_inventory(steamid, inventory)

def add_item(steamid : str, item_name: str, item_type: str, quantity: int):
    database.create_item(item_name, item_type)
    database.add_to_inventory(steamid, item_name, quantity, False)

def get_inventory(steamid: str):
    return [{"name":i[0],"quantity":i[1],"price":i[2], "type":i[3]} for i in database.get_inventory(steamid)]



def update_item_price(item_name: str):
    while True:
        try:
            price = search_item_price(item_name)
            break
        except (TypeError,KeyError) as e:
            print(e, "at", item_name)
            # print(price_url)
            with alive_bar(600) as bar:
                for _ in range(600):
                    sleep(0.1)
                    bar()
    database.set_item_price(item_name, price)

def search_item_price(item_name: str):
    price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_name}'
    response = requests.get(price_url, headers=HEADERS)
    price = float(json.loads(response.content)['lowest_price'][:-1].replace(",",".").strip("-"))
    return price

def get_latest_prices():
    return [{"name":i[2],"quantity":i[1],"price":i[0], "total price":round(float(i[1])*float(i[0]),2)} for i in database.get_latest_prices()]
