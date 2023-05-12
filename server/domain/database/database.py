
from flask import render_template

import server



def display():

    users = server.get_users_db()
    for user in users:
        user["sum"] = f"{user['sum']} ({user['unique']})"
        user["unique"] = user['total']
        user.pop()
    
    total, items = server.get_latest_prices()
    items = [i.values() for i in items]

    profile_items = [ i.values() for i in  server.profile_items() ]
    return render_template("database/database.html", title="Database", users=users, items=items, profile_items=profile_items)


