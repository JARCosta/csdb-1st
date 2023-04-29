
from flask import render_template

import server



def display():
    data = server.get_latest_prices()
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
    return render_template("prices/prices.html", title="Prices", cursor=data)


def update():
    items = server.get_item_list()
    for i in items:
        server.update_item_price(i["name"])
    return render_template("redirect_to_root.html", title="Update Prices")
