from flask import render_template, session
import psycopg2
from psycopg2.extras import DictCursor

from utils.dbConnection import get_db_connection_string
from utils.log import log_join


def update_inv():
    return render_template("redirect_to_root.html", title="Update Inventory")

def display():
    # dbConn = None
    # cursor = None
    try:
        # dbConn = psycopg2.connect(get_db_connection_string())
        # cursor = dbConn.cursor(cursor_factory=DictCursor)
        data = []
        # cursor.execute("SELECT * FROM team;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM game;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM player;")
        # data.append(len(list(cursor)))

        # cursor.execute("SELECT * FROM game WHERE loaded = 0")
        # data.append(len(list(cursor)))
        
        log_join(session["user_id"])
        
        return render_template("root/index.html", result=data, title="Hellow")
    finally:
        # cursor.close()
        # dbConn.close()
        print("")