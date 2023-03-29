

import json


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
        for entry in inventory:
            item, quantity = entry.values()
            self.inventory[item.id] = {"item":item, "quantity":quantity, "total_price":round(item.price*quantity, 2)}

    def export_to_json(self, filename):
        user_dict = {}

        for item in self.inventory.values():
            item, quantity, total_price = item["item"], item["quantity"], item["total_price"]
            user_dict[item.id] = {
                "item": item.to_dic(),
                "quantity": quantity,
                "price": item.price,
                "total_price": total_price
            }
        with open(filename, "w") as f:
            json.dump(user_dict, f, indent=4)

users = [
    User("Jar", "76561198285623099"),
    User("Navi", "76561198185395854"),
    User("Pulga", "76561198201367491")
]


# item1 = Item("1" ,"Item 1", "Type A", 10.0)
# item2 = Item("2", "Item 2", "Type B", 20.0)

# inventory = []

# inventory.append({"item":item1, "quantity":5})
# inventory.append({"item":item2, "quantity":3})


# print(inventory)

# export_to_json()
    

# users[1].set_inventory(inventory)

# users[1].export_to_json("aaa.json")


