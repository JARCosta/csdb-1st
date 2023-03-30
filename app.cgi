#!/usr/bin/python3
from urllib.robotparser import RequestRate
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras

## SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "istnumber"
DB_DATABASE = DB_USER
DB_PASSWORD = "password"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
    DB_HOST,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
)

app = Flask(__name__)

@app.route("/")
def root():
    try:
        return render_template("root.html")
    except Exception as e:
        return str(e)  # Renders a page with the error.



CGIHandler().run(app)
