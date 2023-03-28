import json
import os
from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor
import requests
from domain.inventory import inventoryImpl


from utils.dbConnection import get_db_connection_string
from utils.log import log_join
import v2 as v2

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://steamcommunity.com/',
    'Connection': 'keep-alive',
    # TODO in server: get cookies from browser
    'Cookie':'''sessionid=e02317942bd01b0cc73283e8; cookieSettings={"version":1,"preference_state":2,"content_customization":null,"valve_analytics":null,"third_party_analytics":null,"third_party_content":null,"utm_enabled":true}; browserid=2825485845585510381; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":0,"time_checked":1679780044}; strInventoryLastContext=730_2; timezoneOffset=3600,0; steamDidLoginRefresh=1680024977; steamCountry=PT|7622fb70dbc7c719ac7f7e9a46043d42; steamLoginSecure=76561198285623099||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQyMl8yMjQ3RjZFM19ERTFDOSIsICJzdWIiOiAiNzY1NjExOTgyODU2MjMwOTkiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MDExMjYyNiwgIm5iZiI6IDE2NzEzODQ5ODEsICJpYXQiOiAxNjgwMDI0OTgxLCAianRpIjogIjBEMjdfMjI0QkQyM0ZfRjI0MjMiLCAib2F0IjogMTY3OTc4MDAwOSwgInJ0X2V4cCI6IDE2OTc4Mzc0MDMsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NS45My4yNDIuMTQ0IiwgImlwX2NvbmZpcm1lciI6ICI5NS45My4yNDIuMTQ0IiB9.4_maWs5Yzrb7Sf-ZoUd0wbRmH2kkDBqfWl1_2DHGazNZSBUvhZhHkUwOS1GJts5nss-2meWac8lv_Z2NcJ6_BQ'''
}


def update_inv():
    #TODO: implement
    return render_template("redirect_to_root.html", title="Update Inventory")


def get_page():
    data = []
    for i in v2.get_steam_profiles():
        data.append(i)

    return render_template("inventory/steamids.html", title="Inventory", cursor=data)

def get_inventory_for_steamid(steamid):
    inv = inventoryImpl.get_inventory(steamid)
   
    data = []
    total_price = 0
    quantity = 0
    for i in inv:
        data.append(inv[i])
        quantity += inv[i]["quantity"]
        total_price += inv[i]["total price"]
    data.append({"name": "Total", "quantity": quantity, "total price": round(total_price,2), "price": round(total_price/quantity, 2)})
    return render_template("inventory/inventory.html", title="Inventory", cursor=data)

def update(steamid):
    inventory_url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"

    response = requests.get(inventory_url, headers=HEADERS)
    content = json.loads(response.content)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']

    inv = inventoryImpl.json_to_inv(inventory, descriptions)

    inventoryImpl.save_inv(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices")





