import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import server
import os
import utils
import csv


def print_function_info(func):
    def wrapper(*args, **kwargs):
        filename = os.path.abspath(__file__)
        line_number = func.__code__.co_firstlineno + 1
        print(f"I am in {filename}:{line_number} in {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@print_function_info
def add_user(steamid:str, name: str):
    return


@print_function_info
def add_users(users: dict):
    return


@print_function_info
def get_user_list():

    myFile = open('memory/users.csv', 'r')
    reader = csv.DictReader(myFile)
    users = []
    for row in reader:
        users.append(row)
    
    myFile.close()

    return users

@print_function_info
def store_user_list(users: list[dict]):

    myFile = open('memory/users.csv', 'w')
    writer = csv.writer(myFile)
    writer.writerow(users[0].keys())
    for user in users:
        writer.writerow(user.values())
    
    myFile.close()

    return


@print_function_info
def get_users_db():
    return




@print_function_info
def get_inventory_price(steamid: str):
    return


@print_function_info
def get_inventory_size(steamid: str):
    return


@print_function_info
def get_inventory_unique_items_size(steamid: str):
    return


@print_function_info
def create_item(item_name: str, item_type: str):
    return


@print_function_info
def get_items():
    return



@print_function_info
def set_item_price(item_name: str, price: int, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    return



@print_function_info
def add_to_inventory(steamid: str, item_name: str, quantity: int, auto: bool):
    return


@print_function_info
def alter_item(steamid, item, quantity):
    return


@print_function_info
def get_inventory(steamid: str):
    return


@print_function_info
def set_inventory(steamid: str, inventory: dict):
    return


@print_function_info
def clear_auto_inventory(steamid: str):
    return


@print_function_info
def get_items_to_update():
    return


@print_function_info
def get_latest_prices():
    return


@print_function_info
def profile_items():
    return


@print_function_info
def delete_item(item_name: str):
    return


