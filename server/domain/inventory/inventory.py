import json
from flask import render_template
import requests
from domain.inventory import inventoryImpl

import server
from utils.headers import HEADERS


def display(steamid: str):
    if not steamid:
        data = [{"name": user["name"],"steamid": user["steamid"]} for user in server.get_users()]
        return render_template("inventory/steamids.html", title="Inventory", cursor=data)
    else:
        data = server.get_inventory(steamid)
        # print(steamid)
        print(data)
        # data = inv
        return render_template("inventory/inventory.html", title="Inventory", cursor=data)


def update(steamid, js):
    if js == None:
        inventory_url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"
        js = requests.get(inventory_url, headers=HEADERS).content

    content = json.loads(js)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']
    
    inv = inventoryImpl.json_to_inv(inventory, descriptions)
    # for i in inv:
    #     print(i, inv[i])
    server.set_inventory(steamid, inv)
    inventoryImpl.save_inv(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices")












