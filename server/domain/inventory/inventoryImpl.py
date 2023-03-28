





from datetime import datetime
import json
import os
import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://steamcommunity.com/',
    'Connection': 'keep-alive',
    # TODO in server: get cookies from browser
    'Cookie':'''sessionid=e02317942bd01b0cc73283e8; cookieSettings={"version":1,"preference_state":2,"content_customization":null,"valve_analytics":null,"third_party_analytics":null,"third_party_content":null,"utm_enabled":true}; browserid=2825485845585510381; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":0,"time_checked":1679780044}; strInventoryLastContext=730_2; timezoneOffset=3600,0; steamDidLoginRefresh=1679914832; steamCountry=PT|5f29ea7663fb0e8818d774d49c5bafca; steamLoginSecure=76561198285623099||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQyMl8yMjQ3RjZFM19ERTFDOSIsICJzdWIiOiAiNzY1NjExOTgyODU2MjMwOTkiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MDAwMjcwMiwgIm5iZiI6IDE2NzEyNzQ4MzMsICJpYXQiOiAxNjc5OTE0ODMzLCAianRpIjogIjBEMjdfMjI0N0Y4ODBfMzAwOTgiLCAib2F0IjogMTY3OTc4MDAwOSwgInJ0X2V4cCI6IDE2OTc4Mzc0MDMsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NS45My4yNDIuMTQ0IiwgImlwX2NvbmZpcm1lciI6ICI5NS45My4yNDIuMTQ0IiB9.rWBjLOET3hyvX61cCp79gJx7KiMUVbtOzoeZ0lLsURcJa4P37JmjVv5HGxzCm6uY9SQZCvBa_kQBJTDRAUO4CQ'''
}

def get_inventory(STEAMID: str):
    dir_path = './saves/' + STEAMID
    files = sorted(os.listdir(dir_path))
    files.reverse()
    try:
        print("loading last save:", files[0])
        file = open(dir_path + "/" + files[0], 'r',encoding='utf-8')
        inv = dict(json.load(file))
        file.close()
        inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
        return inv
    except IndexError:
        # print("no save found")
        return {}

def json_to_inv(inventory: dict, descriptions: dict):
    inv = {}

    for item in descriptions:
        values = descriptions[item]
        if values["marketable"] == 1:
            temp = {
                    "quantity": 0,
                    "name" : values["market_hash_name"],
                    # "name_color" : "#" + values["name_color"],
                    "type": values["type"],
                    # "price": 0.00,
                    # "total price": 0.00
                }
            inv[values["market_hash_name"]] = temp

    for item in inventory:
        item_key = inventory[item]['classid'] + "_" + inventory[item]['instanceid']
        try:
            inv[item_key]['quantity'] += 1
        except:
            pass

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
    return inv


def save_inv(STEAMID: str, inv: dict):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name =f"saves/{STEAMID}/{time}.json"

    print("saving :", file_name)
    with open(file_name,'w',encoding='utf-8') as file:
        file.write(json.dumps(inv, indent=4))
        file.close()




