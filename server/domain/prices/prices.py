
from alive_progress import alive_bar
from flask import render_template
from time import sleep

import server



def display():
    data = server.get_latest_prices()
    return render_template("prices/prices.html", title="Prices", cursor=data)


def update():
    items = server.get_item_list()
    for i in items:
        while True:
            try:
                server.add_item_price(i["name"])
                break
            except TypeError:
                print("TypeError at",i["name"])
                with alive_bar(600) as bar:
                    for _ in range(600):
                        sleep(0.1)
                        bar()
            except KeyError:
                print("KeyError at",i["name"])
                with alive_bar(100) as bar:
                    for _ in range(100):
                        sleep(0.1)
                        bar()
    return render_template("redirect_to_root.html", title="Update Prices")
