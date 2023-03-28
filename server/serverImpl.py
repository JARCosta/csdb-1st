import hashlib
import time
from flask import Flask, request, session
import domain

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
    return domain.root.get_main_page()


@app.route("/inventory")
def inventory():
    steamid = request.args.get('steamid')
    if steamid:
        return domain.inventory.get_inventory_for_steamid(steamid)
    else:
        return domain.inventory.get_page()

@app.route("/inventory/update", methods=['POST'])
def inv_update():
    if request.method == 'POST':
        steamid = request.form["steamid"]
        json = request.form["json"]
        if json == "null":
            return domain.inventory.update(steamid, None)
        else:
            return domain.inventory.update(steamid, json)


@app.route("/prices")
def prices():
    return domain.prices.get_page()

@app.route("/prices/update")
def prices_update():
    return domain.prices.update()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

