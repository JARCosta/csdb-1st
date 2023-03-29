

from datetime import datetime
import json
import os
import database

class Item:
    def __init__(self,item_id: str, name: str, item_type: str, price: float):
        self.id = item_id
        self.name = name
        self.item_type = item_type
        self.price = price
    
    def to_dic(self):
        return {"name": self.name, "type": self.item_type, "price": self.price}

class User:
    def __init__(self, name: str, steamid: str):
        self.name = name
        self.steamid = steamid
        self.inventory = {}
    
    def set_inventory(self, inventory: dict):
        # for entry in inventory:
        #     item, quantity = entry.values()
        #     self.inventory[item.id] = {"item":item, "quantity":quantity, "total_price":round(item.price*quantity, 2)}
        self.inventory = {}
        for entry in inventory:
            item = inventory[entry]
            self.inventory[item["name"]] = {"item":Item(item["name"],item["name"], item["type"], 0), "quantity":item["quantity"]} #TODO price

    def inventory_to_dict(self):
        export_dict = {}
        inventory = [(entry["item"], entry["quantity"]) for entry in self.inventory.values()]
        for item, quantity in inventory:
            # print(item.id, quantity)
            export_dict[item.id] = {
                "item": item.to_dic(),
                "quantity": quantity,
                "price": item.price,
                "total_price": round(quantity*item.price,2)
            }
                     
        # for item, quantity, total_price in [(item["item"], item["quantity"], item["total_price"]) for item in self.inventory.values()]:
        #     export_dict[item.id] = {
        #         "item": item.to_dic(),
        #         "quantity": quantity,
        #         "price": item.price,
        #         "total_price": total_price
        #     }
        return export_dict

    def load_inventory(self):
        dir_path = './saves/' + self.steamid
        files = sorted(os.listdir(dir_path))
        files.reverse()
        try:
            print("loading last save:", files[0])
            with open(dir_path + "/" + files[0], 'r',encoding='utf-8') as file:
                inv = dict(json.load(file))
            inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
            self.set_inventory(inv)
        except IndexError:
            # print("no save found")
            return {}

    def export_to_json(self):
        export_dict = self.inventory_to_dict()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name =f"saves/{self.steamid}/{time}.json"
        print("saving :", file_name)
        with open(file_name, "w") as f:
            json.dump(export_dict, f, indent=4)


users = [
    User("Jar", "76561198285623099"),
    User("Navi", "76561198185395854"),
    User("Pulga", "76561198201367491")
]


def add_user(name: str, steamid: str):
    users.append(User(name, steamid))

def get_users():
    return [user for user in users]

def get_names():
    return [user.name for user in users]
    list = []
    for user in users:
        print(user)
        list.append(user.name)
        # list.append(user["name"])
    return list

def get_ids():
    return [user.steamid for user in users]
    list = []
    for user in users:
        print(user)
        list.append(user.steamid)
        list.append(user["steamid"])
    return list

# def get_user_inventory(steamid: str):
#     dir_path = './saves/' + steamid
#     files = sorted(os.listdir(dir_path))
#     files.reverse()
#     try:
#         print("loading last save:", files[0])
#         file = open(dir_path + "/" + files[0], 'r',encoding='utf-8')
#         inv = dict(json.load(file))
#         file.close()
#         inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
#         return inv
#     except IndexError:
#         # print("no save found")
#         return {}

def get_user_inventory(steamid: str):
    for user in users:
        if user.steamid == steamid:
            user.load_inventory()
            return user.inventory_to_dict()

def get_all_items():
    all_items = {}
    for user in users:
        for item in user.inventory:
            all_items[item.id] = item
    return all_items
