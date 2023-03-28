from datetime import datetime
import json
import os
from alive_progress import alive_bar
from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor
import requests
from domain.inventory import inventoryImpl
from time import sleep
import time

from utils.dbConnection import get_db_connection_string
from utils.log import log_join
from utils.headers import HEADERS
import server

def get_prices():
    dir_path = './saves/prices'
    files = sorted(os.listdir(dir_path))
    files.reverse()
    try:
        print("loading last prices:", files[0])
        file = open(dir_path + "/" + files[0], 'r',encoding='utf-8')
        prices = json.load(file)
        file.close()
        return dict(prices)
    except IndexError:
        # print("no prices found")
        return {}


def load_items():
    item_map = {}
    for steamid in server.get_steam_ids():
        inv = inventoryImpl.get_inventory(steamid)
        for index in inv:
            try:
                item_map[inv[index]["name"]]["quantity"] += inv[index]["quantity"]
            except:
                item_map[inv[index]["name"]] = inv[index]
    
    item_map = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
    return item_map # has all the items to be updated


def get_page():
    data = []
    dic = load_items()
    # inv = dict(sorted(dic.items(), key=lambda item: item[1]["total price"], reverse=True))
    inv = dict(sorted(dic.items(), key=lambda item: item[1]["quantity"], reverse=True))
    
    for i in inv:
        data.append(inv[i])
    return render_template("prices/prices.html", title="Prices", cursor=data)


def update():
    item_map = load_items()
    try:
        del item_map['quantity']
        del item_map['total price']
    except:
        pass
    
    for item in item_map:
        while True:
            try:
                price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_map[item]["name"]}'
                response = requests.get(price_url, headers=HEADERS)
                print(response.text, item["name"])
                lowest_price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))
                # print("updating", item_map[item]["name"], "new price", lowest_price)
                item_map[item]["price"] = lowest_price
                break
            except TypeError as e:
                print(price_url)
                with alive_bar(600) as bar:
                    for _ in range(600):
                        sleep(0.1)
                        bar()
            except KeyError:
                print("KeyError", item_map[item]["name"], "\n", price_url)


    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name =f"saves/prices/{time}.json"

    print("saving :", file_name)
    with open(file_name,'w',encoding='utf-8') as file:
        file.write(json.dumps(item_map, indent=4))
        file.close()

    #TODO: update prices in db
    return render_template("redirect_to_root.html", title="Update Prices")
