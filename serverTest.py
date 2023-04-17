from flask import render_template
import psycopg2
from psycopg2.extras import DictCursor
import utils

from urllib.robotparser import RequestRate
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras


DB_CONNECTION_STRING = utils.get_db_connection_string()

def get_users():
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM profiles;")
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

def get_inventory(steamid: str):
    return [{"name":i[0],"quantity":i[1],"price":i[2]} for i in database_get_inventory(steamid)]

def database_get_inventory(steamid: str):
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=DictCursor)
        querry = f"""
            SELECT ip.item, quantity, price
            FROM item_prices ip
            JOIN (
            SELECT item, MAX(date) AS max_date
            FROM item_prices
            GROUP BY item
            ) latest ON ip.item = latest.item AND ip.date = latest.max_date
            JOIN profile_items ON profile_items.item = ip.item
            WHERE profile = '{steamid}';
            """
        cursor.execute(querry)
        return cursor.fetchall()
    finally:
        cursor.close()
        dbConn.close()

