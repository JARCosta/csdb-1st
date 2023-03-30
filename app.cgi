#!/usr/bin/python3
from urllib.robotparser import RequestRate
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from difflib import get_close_matches
from time import sleep
import time
from difflib import SequenceMatcher


import psycopg2
import psycopg2.extras
from time import sleep
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.model_selection import train_test_split

## SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist199088"
DB_DATABASE = DB_USER
DB_PASSWORD = "jackers"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
    DB_HOST,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
)

app = Flask(__name__)


@app.route("/")
def root():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        return render_template("index.html", title="Test")
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()



CGIHandler().run(app)
