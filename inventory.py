import json
from flask import render_template
import requests

import serverTest
import utils
import database

def test(steamid: str):
    if not steamid:
        data = [{"name": user["name"],"steamid": user["steamid"]} for user in serverTest.get_users()]
        return render_template("steamids.html", title="Inventory", cursor=data, homeURL=utils.HOME_URL)
    else:
        data = []
        for i in serverTest.get_inventory(steamid):
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
        return render_template("inventory.html", title="Inventory", cursor=data, homeURL=utils.HOME_URL)

def display(steamid: str):
    if not steamid:
        data = [{"name": user["name"],"steamid": user["steamid"]} for user in server.get_users()]
        return render_template("inventory/steamids.html", title="Inventory", cursor=data, homeURL=utils.HOME_URL)
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
        return render_template("inventory.html", title="Inventory", cursor=data, homeURL=utils.HOME_URL)


def update(steamid, js):
    if js == None:
        inventory_url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"
        js = requests.get(inventory_url, headers=utils.HEADERS).content

    content = json.loads(js)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']

    inv = json_to_inv(inventory, descriptions)
    # for i in inv:
    #     print(i, inv[i])
    database.set_inventory(steamid, inv)
    # inventoryImpl.save_inv(steamid, inv)

    return render_template("redirect_to_root.html", title="Update Prices", homeURL=utils.HOME_URL)


def json_to_inv(inventory: dict, descriptions: dict):
    inv = {}

    for item in descriptions:
        values = descriptions[item]
        if values["marketable"] == 1:
            temp = {
                    "quantity": 0,
                    "name" : values["market_hash_name"],
                    # "name_color" : "#" + values["name_color"],
                    "type": values["type"],
                    # "price": 0.00,
                    # "total price": 0.00
                }
            inv[item] = temp

    for item in inventory:
        item_key = inventory[item]['classid'] + "_" + inventory[item]['instanceid']
        try:
            inv[item_key]['quantity'] += 1
        except:
            pass

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))

    ret_dic = {}
    for item in inv:
        try:
            ret_dic[inv[item]["name"]]["quantity"] += inv[item]["quantity"]
        except:
            ret_dic[inv[item]["name"]] = inv[item]



    return ret_dic

