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
        data = []
        for i in server.get_inventory(steamid):
            temp = i
            temp["total price"] = round( i["quantity"] * i["price"] ,2)
            data.append(temp)
        data.sort(key=lambda x: x['total price'])
        data.reverse()

        total_items = 0
        total_price = 0
        for i in data:
            total_items += i["quantity"]
            total_price += i["total price"]
        if total_items > 0:
            average_price = total_price/total_items
        else:
            average_price = 0
        
        new_data = [{"name":"Total","quantity":total_items,"price":round(average_price,2),"total price":round(total_price,2)}]
        new_data.extend(data)
        data = new_data
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
    # inventoryImpl.save_inv(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices")












