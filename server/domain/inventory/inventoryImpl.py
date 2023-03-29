





from datetime import datetime
import json
import os
import requests


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

