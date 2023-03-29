

from datetime import datetime
import json
import os

import requests
import database
from utils.headers import HEADERS


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



def get_inventory(steamid: str):
    return [{"user":i[0],"name":i[1],"quantity":i[2],"price":i[3]} for i in database.get_inventory(steamid)]

def set_inventory(steamid: str, inventory: dict):
    return database.set_inventory(steamid, inventory)

def get_item_list():
    return [{"name":i[0],"type":i[1]} for i in database.get_item_list()]


def add_item_price(item_name: str):
    price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_name}'
    response = requests.get(price_url, headers=HEADERS)
    price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.add_item_price(item_name, price, time)

def get_prices():
    return [{"name":i[0],"quantity":i[2],"price":i[1]} for i in database.get_prices()]
