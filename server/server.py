#!/usr/bin/python3

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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

