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
            i["total price"] = round( i["quantity"] * (i["price"] or 0) ,2)
            data.append(i)
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

        type_selection = list(set([i["type"] for i in data[1:]]))
        # print(type_selection)


        return render_template("inventory/inventory.html", title="Inventory", cursor=data, steamid=steamid, type_selection=type_selection)

def add(steamid: str, item_name: str, item_type: str, quantity: int):
    if item_name.__contains__("https://steamcommunity.com/market/listings/730/"):
        item_name = item_name.replace("https://steamcommunity.com/market/listings/730/","")
    server.add_item(steamid,item_name,item_type, quantity)
    return render_template("redirect.html", title="Add Item", page = "inventory?steamid=" + steamid)


def json_to_inv(inventory: dict, descriptions: dict):
    inv = {}

    # create a dictionary with all the items in the inventory
    for item in descriptions:
        values = descriptions[item]
        if values["marketable"] == 1:

            type =  values["tags"][1]["category"]
            if type == "Quality" or type == "ItemSet":
                type =  values["tags"][0]["name"]
            inv[item] = {
                    "quantity": 0,
                    "name" : values["market_hash_name"],
                    "type": type,
                }

    # set the quantity of each item
    for item in inventory:
        try:
            item_key = inventory[item]['classid'] + "_" + inventory[item]['instanceid']
            inv[item_key]['quantity'] += 1
        except:
            pass

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))

    # merge items with the same name
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

    return render_template("redirect.html", title="Update Prices", page = "inventory?steamid=" + steamid)




def alter(steamid, item, quantity):
    server.alter_item(steamid, item, quantity)
    return display(steamid)
    return render_template("redirect.html", title="Update Prices", page = "inventory?steamid=" + steamid)
    return str([steamid, item, quantity])





