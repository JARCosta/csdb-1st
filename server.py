

from datetime import datetime
import json
from alive_progress import alive_bar
from time import sleep

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
    return [{"name":i[0],"quantity":i[1],"price":i[2]} for i in database.get_inventory(steamid)]

def set_inventory(steamid: str, inventory: dict):
    return database.set_inventory(steamid, inventory)

def get_item_list():
    return [{"name":i[0],"type":i[1]} for i in database.get_item_list()]


def add_item_price(item_name: str):
    price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_name}'
    while True:
        try:
            response = requests.get(price_url, headers=HEADERS)
            price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))
            break
        except (TypeError,KeyError) as e:
            print(e, "at", item_name, "\n", price_url)
            with alive_bar(600) as bar:
                for _ in range(600):
                    sleep(0.1)
                    bar()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.add_item_price(item_name, price, time)

def get_latest_prices():
    return [{"name":i[2],"quantity":i[1],"price":i[0], "total price":round(float(i[1])*float(i[0]),2)} for i in database.get_latest_prices()]
