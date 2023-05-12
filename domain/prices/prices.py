
from flask import render_template

import server



def display():
    total,data = server.get_latest_prices()
    
    total.extend(data)
    data = total

    return render_template("prices/prices.html", title="Prices", cursor=data)


def update():
    items = server.get_item_list()
    for i in items:
        server.update_item_price(i["name"])
    return render_template("redirect_to_root.html", title="Update Prices")
