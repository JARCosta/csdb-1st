import json
from flask import render_template
import requests

import server
from utils import HEADERS


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
        print(data)
        return render_template("inventory/inventory.html", title="Inventory", cursor=data)


def json_to_inv(inventory: dict, descriptions: dict):
    inv = {}

    for item in descriptions:
        values = descriptions[item]
        if values["marketable"] == 1:
            inv[item] = {
                    "quantity": 0,
                    "name" : values["market_hash_name"],
                    "type": values["type"],
                }

    for item in inventory:
        try:
            item_key = inventory[item]['classid'] + "_" + inventory[item]['instanceid']
            inv[item_key]['quantity'] += 1
        except:
            pass

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))


    ret_dic = {}
    for item in inv: # for each element change its key from classid to market_hash_name
        try:
            ret_dic[inv[item]["name"]]["quantity"] += inv[item]["quantity"]
            print("" + inv[item]["name"] + "\033[31m is repeated, summing quantities \033[0m")
        except:
            ret_dic[inv[item]["name"]] = inv[item]
            print("" + inv[item]["name"] + "\033[32m adding new item \033[0m")

    return ret_dic


def update(steamid, js):
    if js == None:
        inventory_url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"
        js = requests.get(inventory_url, headers=HEADERS).content

    content = json.loads(js)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']
    
    inv = json_to_inv(inventory, descriptions)
    server.set_inventory(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices")












