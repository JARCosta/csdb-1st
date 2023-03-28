import json
import os
from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor

from utils.dbConnection import get_db_connection_string
from utils.log import log_join
import v2 as v2

def load_last_save(STEAMID: str):
    dir_path = './saves/' + STEAMID
    files = sorted(os.listdir(dir_path))
    files.reverse()
    print("loading last save:", files[0])
    file = open(dir_path + "/" + files[0], 'r',encoding='utf-8')
    js = json.load(file)
    file.close()
    return js

def update_inv():
    inv_map = {}
    for steamid in v2.get_steam_ids():
        inv = load_last_save(steamid)
        for index in inv:
            try:
                inv_map[inv[index]["name"]]["quantity"] += inv[index]["quantity"]
            except:
                inv_map[inv[index]["name"]] = inv[index]
    for i in inv_map:
        print(inv_map[i]["name"], inv_map[i]["quantity"])
    
    # inv_map = dict(sorted(inv_map.items(), key=lambda item: item[1]["quantity"], reverse=True))
    
    return render_template("redirect_to_root.html", title="Update Inventory")

def

def get_page():
    # dbConn = None
    # cursor = None
    # try:
        # dbConn = psycopg2.connect(get_db_connection_string())
        # cursor = dbConn.cursor(cursor_factory=DictCursor)
        # data = []
        # cursor.execute("SELECT * FROM team;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM game;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM player;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM game WHERE loaded = 0")
        # data.append(len(list(cursor)))
        
        # log_join(session["user_id"])
        
        #return str([len(teams), len(games), len(players)])
    data = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    return render_template("inventory/inventory.html", title="Inventory", cursor=data)
    # except Exception as e:
    #     raise e  # Renders a page with the error.
    # finally:
        # cursor.close()
        # dbConn.close()