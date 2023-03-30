#!/usr/bin/env python3

import hashlib
import time
from flask import Flask, request, session
import domain
import server

app = Flask(__name__, template_folder='domain', static_folder='domain/static')
app.secret_key = 'your_secret_key'

@app.before_request
def before_request():
    if 'user_id' not in session:
        ip = request.remote_addr
        current_time = time.time()
        user_id = hashlib.md5(f'{ip}{current_time}'.encode()).hexdigest()
        session['user_id'] = user_id

@app.route("/")
def root():
    return domain.root.display()


@app.route("/inventory", methods=["GET"])
def inventory():
    steamid = request.args.get('steamid') or None
    return domain.inventory.display(steamid)

@app.route("/inventory/update", methods=['POST'])
def inv_update():
    steamid = request.form["steamid"]
    try:
        json = request.form["json"]
    except KeyError:
        json = None
    return domain.inventory.update(steamid, json)


@app.route("/prices")
def prices():
    return domain.prices.display()

@app.route("/prices/update")
def prices_update():
    return domain.prices.update()


if __name__ == '__main__':
    server.__init__()
    app.run(debug=True, use_reloader=True)

