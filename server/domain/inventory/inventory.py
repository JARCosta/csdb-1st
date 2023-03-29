import json
import os
from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor
import requests
from domain.inventory import inventoryImpl


from utils.dbConnection import get_db_connection_string
from utils.log import log_join
import server
import domain
from utils.headers import HEADERS


def update_inv():
    #TODO: implement
    return render_template("redirect_to_root.html", title="Update Inventory")

def display(steamid: str):
    if not steamid:
        data = [{"name": user.name,"steamid": user.steamid} for user in server.get_users()]
        return render_template("inventory/steamids.html", title="Inventory", cursor=data)
    else:
        inv = server.get_user_inventory(steamid)
        print(inv)
        data = []
        return render_template("inventory/inventory.html", title="Inventory", cursor=data)


def get_page():
    data = []
    for i in server.get_steam_profiles():
        data.append(i)

    return render_template("inventory/steamids.html", title="Inventory", cursor=data)

def get_inventory_for_steamid(steamid):
    inv = inventoryImpl.get_inventory(steamid)
   
    prices = domain.prices.get_prices()

    data = []
    total_price = 0
    quantity = 0
    for i in inv:
        data.append(inv[i])
        quantity += inv[i]["quantity"]
        total_price += round(prices[i]["price"] * inv[i]["quantity"], 2)
    data.append({"name": "Total", "quantity": quantity, "total price": round(total_price,2), "price": round(total_price/quantity, 2)})
    return render_template("inventory/inventory.html", title="Inventory", cursor=data)

def update(steamid, js):
    if js == None:
        inventory_url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"
        js = requests.get(inventory_url, headers=HEADERS).content

    content = json.loads(js)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']
        
    inv = inventoryImpl.json_to_inv(inventory, descriptions)

    inventoryImpl.save_inv(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices")












