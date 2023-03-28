import json
import os
from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor
from domain.inventory import inventoryImpl

from utils.dbConnection import get_db_connection_string
from utils.log import log_join
from domain import serverImpl

def load_prices():
    inv_map = {}
    for steamid in serverImpl.get_steam_ids():
        inv = inventoryImpl.get_inventory(steamid)
        
        for index in inv:
            try:
                inv_map[inv[index]["name"]]["quantity"] += inv[index]["quantity"]
            except:
                inv_map[inv[index]["name"]] = inv[index]
    
    return inv_map # has all the items to be updated


def get_page():
    data = []
    dic = load_prices()
    inv_by_total_price = dict(sorted(dic.items(), key=lambda item: item[1]["total price"], reverse=True))
    inv_by_quantity = dict(sorted(dic.items(), key=lambda item: item[1]["quantity"], reverse=True))
    
    inv = inv_by_total_price
    for i in inv:
        data.append(inv[i])
    return render_template("prices/prices.html", title="Prices", cursor=data)


def update():
    inv_map = load_prices()
    #TODO: update prices in db
    return render_template("redirect_to_root.html", title="Update Prices")


