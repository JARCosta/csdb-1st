from datetime import datetime
import json
from time import sleep
from flask import render_template

import requests
import database
import utils

def get_latest_prices():
    return [{"name":i[2],"quantity":i[1],"price":i[0], "total price":round(float(i[1])*float(i[0]),2)} for i in database.get_latest_prices()]

def display():
    data = get_latest_prices()
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
    return render_template("prices.html", title="Prices", cursor=data, homeURL=utils.HOME_URL)

def get_item_list():
    return [{"name":i[0],"type":i[1]} for i in database.get_item_list()]

def add_item_price(item_name: str, time: datetime):
    price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={item_name}'
    while True:
        try:
            response = requests.get(price_url, headers=utils.HEADERS)
            price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))
            break
        except (TypeError,KeyError) as e:
            print(e, "at", item_name, "\n", price_url)
            sleep(60))
    database.add_item_price(item_name, price, time)

def update():
    items = get_item_list()
    time = datetime.now().strftime("%H:%M %d-%m-%y")
    for i in items:
        add_item_price(i["name"], time)
    return render_template("redirect_to_root.html", title="Update Prices", homeURL=utils.HOME_URL)
