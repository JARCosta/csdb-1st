import json
import os
from time import sleep
import time
import requests
from datetime import datetime
from tqdm.notebook import tqdm
from alive_progress import alive_bar

from re import finditer
from matplotlib import legend
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from difflib import get_close_matches
from time import sleep
import time
from difflib import SequenceMatcher
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from math import fsum, ceil

import debug

STEAMID = "76561198185395854" # NAVi
STEAMID2 = "76561198285623099" # JAR


URL = f"https://steamcommunity.com/profiles/{STEAMID}/inventory/json/730/2"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://steamcommunity.com/',
    'Connection': 'keep-alive',
    # TODO in server: get cookies from browser
    'Cookie':'''__Host-next-auth.csrf-token=386399fbc684bf95998a4ab2ab51dfa376eff75fb41f2771b80ff710ebf2b5c2|f9dcf530750ec994b08f994dd9a0a200f57e12cb2cfafed274cc4f70cdaee4c5; _ga=GA1.1.650911837.1678913476; oai-asdf-ugss=user-sCudUHXgaCRREjSzYBtXiEML; oai-asdf-gsspc=user-sCudUHXgaCRREjSzYBtXiEML; __Secure-next-auth.callback-url=https://chat.openai.com/chat; oai-asdf-nacb=user-sCudUHXgaCRREjSzYBtXiEML; _ga_9YTZJE58M9=GS1.1.1679602260.5.0.1679602271.0.0.0; _cfuvid=SlyqoTva_qpzwtYF7eLUEzfMEHZkGjVNPioA38iODPs-1679929448923-0-604800000; cf_clearance=Vhl2Vhc0STIUcrpAcksbbIM69PWNJoCR0eSUtotsU.U-1680015009-0-1-6e1ca9a1.bab140dc.9b8649d6-160; intercom-device-id-dgkjq2bp=9d273765-1330-4c2e-a05f-9ecc27f691f7; cf_clearance=RylLnzq1kqtWYS0hptYemwf5EgRsB4xAZlhMwfM9f3E-1680017825-0-1-6e1ca9a1.bab140dc.9b8649d6-160; intercom-session-dgkjq2bp=V1Z2eVQ1eHgzUzFTYTlDSUFycmdYQjNUZURGOGFXMmlrNWZIQm1mVmxpSERsTkNpT3M3QmNTTHVTMlIyRkJTOS0td0VGSEV0V1lNT0F3Y1VVNjZPL3FLZz09--411cde7f5bba4691edb1c2e43d90fd239f87f7da; __cf_bm=K8feIWGvxNkZTcWvnXy_EiCx8sXe3XZl0RPNYxtfmxI-1680024724-0-AZE07bTik5IVvMmmQQyEQBeAuo+yHkEBh4s0yaj4pV482DRGgcOEwNEKgV4nFpZ5sTUV3Wl5S6++tbacBZdu2jY=; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..c8f7Qe6hwI75O4oI.eA3Lj83ZnIkiClb3O4uOtqVGcDHl9cbYrnht7k_JZiJVOyr-RAtpH9Dc9Hsja4g8vyMAJ1BDXYldhucHUMFGbCa3AUcoIdj_cbJL9zwl2n-ZLbRggQWzKbz2aFz-DbDCphsS1w4CJWne5zKs91zAIb7fGNyoKOfodNVLEaRARRJZTh4tNLCIgR6To3tJiZpxPLOSdTSN2oMQc6mW4iwMpFSmFMvd0kHBhYOoK6bxywRy54y0gg-R4DmEgt1PfqDFSYdbROqRvdq8dNZAiRICv2d-G_00Mb6g1ttWiMTfD6d1iKH7hMCVzFE31wNR4XsvBBRLmZvkwogyTHpWzRmq0wwRpncQ0QOKmVkY2Re9r3ZXDntXVfjUtf3qHMHEPHwYheCZS_yUCUNi1EoSVwUXDONlWWIjI6U7xWADeu0rnCXf0mtvNnmNE1JmmqiWXFa1DPN3YdPnQM6dYHeF9esRrwnYLMkaUXVIawoOPYKsgjdO_IW72oypJD2y7EbyjsijaGawRxWGx5EYDC0MvOd1sxeCjH04_eZhCTSz_O11bGJ300MRoTzblCPtad8Hkt1a05vr7RHTesCGA4k7ZhTsQTVNepTmtdazBQ2sTTGX4vAlUoSQxp4GRpw2cZUNDYiU0BohZecPaO14IgXv9dWGuzeV8R_iKwncEfGdTLp37d-5bBPKlmMb7wjCU6HfMELtrslzZ5kY4xS-TsH2pwO0vfZeqR4fXhkiEYVQyEuXIpWSeWPDXwVjKxZV41ifnAtFRr1evYfBInRjwRWGstEYNbE3WJpvdmirpLd1miU6YazgICZZIeLx7XtCEeEojJWlCjkaTSkuHey0Z2i7RqyB0hPJdPN_9YiClnLtkwhCPYqJPnwr5eIuo_cqja_be97flvhyAJqKxIG2tt6VkF4y9gUOROxcEo-nV1m2-do3bEDPsAazjE6XB3WHZDqPC9XWS6Q3Gvm9i0F481Ddvlhj4mH4GuB5cSg_K-p2EzBRdwYBdIJ5eXtRZ39IpN3rYUAJwzO-RkhB4zRTpzAvhavfOh6cfDWI054e9jHdNKJP5CY-8iOOwgo60CfseE8ZiKvySJlJstoaP58jPFuWbHk1-Iub2ekSKQdb5dLuokTKFyOcSeE3FPO0CGI5My_6UFpsCiqnIlT8D6z0hX2wSA3oWHOZb6apuUMjgGui4psBt18Ipk5Hu0E7MO1wI1GqT4SKZ3XGUWNNi-KUzyX345cG_KKRwKoaTGWHLovKC42U_qQQmK46vnfOUkj_s8aIFcOuNhOFwNgzS0BmfTQ4Ise-PeJbLCTTfkaeXZvHBM3vkyD3uiUOAY6ZVG1sD9pVCiqf7LihTSjWgPcHdfOZ5qNMbV-ZgBFz7X2NooDwV8GMirowPko-BDMCX2b5SS2UljvlqOYIu3J_EBUaMvq1DvqN56vO78Qf6DoyTNS5RypBhYvZHssthX-pU2drHYNBlLNe6WK-bF2frGbekvNEflwri6W1JRRX5cvl3Icii-q4ZUKvF5haZnC-V3AUR3SoORoGWE7L09osiLdeRBJJ-xCnjvBkxsN0VMTZMZKNAgJSZm6f_oRBCnAXXw8QP5G2gqi7n-l-89UPL5H2k2vUBKzEDPX0biRsf0sPqLtECXb7NnBZzmD9sNgCGHbblUGqzAed1TlCzxXYpigNLHpf-ERQ_u4M_RIv7B_ut4i1uZHCX1DIFdPU6duX5-S3snFsPqMyoHT-vqfLY0N0KVkb7wwAT7LYRf-FLgejiO0jSjz3o-nQ_QdnEniyRhZ7XNwnJbRBFMN_hAJqoQ1dj4p3qnV4clSewx5YCuydIBJ_j9ntuqF9tiwTca26Z5zZHra0Lu-kuMq8vNwwmFQSVeogHWIE5wjNa0olULFfs1wh1RE2Bmtv5TVe10qKiDXzDGdZHc-mOLxsEPzKTT28AyS5kyxQus51X6I7RaVfzSDJOjcDn7uxyrRU0SGMGBC7e0dt2wy9gzO4_XeBK_B-9rXiNHI2mrc9J5hrklvEyW83lRanBoCpZgb6e3sfguU3-nFVnGujmXXHANohq30xAH1cQamckWWYPTPC8udxcMx5Qt8nR25LnAd7zLk5lDdVs3OS-W21RSfPlQ_repqrRxcndJ8yb1kLrrJfe79_F7LzVr2jb_jUgvQN0KPgbpHjSRovcWwy8gpcuYnTxmgJI-5CclQC362PwtbVRzjYsQfCuuawEVHh3HD0V2wA2alEfc_K8OpaxUkYWbzNeR7bjX3EIjzKfXAvu83i-qzC_Y6uxV5jBkIMc9lVL2hseorS_x1kOSvnMaZdlPsOSJz_Qj0Zese5_ffbXqktfGmLKj7Toq3jc1NXr_Pu12taaz8ZBuM5wRpdVztB1zdaM5CQwLJUhMpMJL7M4g9qJ6ZRR6Y4vNcFTgtSkbOKNQNVDzdCaztZKRgmFQ7S_v3oFje6aRP7AlsbGNY0aV4gWbLlz90SlM52FK6h21g.rJoa4b07lcNlBe2D-GCePA'''
}

steam_profiles = [{"name": "NAVi", "steamid": "76561198185395854"}, {"name": "JAR", "steamid": "76561198285623099"}]

def add_steam_profile(name: str, steamid: str):
    steam_profiles.append({"name": name, "steamid": steamid})

def get_steam_profiles():
    return steam_profiles

def get_steam_ids():
    return [profile["steamid"] for profile in steam_profiles]

def inv_import(file: str):
    with open(file,'r',encoding='utf-8') as file:
        inv = json.load(file)
        file.close()
    return inv

def save_inv(STEAMID: str, inv: dict):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name =f"saves/{STEAMID}/{time}.json"

    print("saving :", file_name)
    with open(file_name,'w',encoding='utf-8') as file:
        file.write(json.dumps(inv, indent=4))
        file.close()


def file_to_json(dir: str):
    with open(dir,'r',encoding='utf-8') as file:
        file = json.load(file)
        file.close()
    inventory, descriptions = file["rgInventory"] , file["rgDescriptions"]
    return inventory, descriptions

def url_to_json(url: str):
    print(url)
    response = requests.get(url, headers=HEADERS)
    content = json.loads(response.content)
    inventory, descriptions = content['rgInventory'], content['rgDescriptions']
    return inventory, descriptions

def json_to_inv(inventory, descriptions):
    inv = {}

    for item in descriptions:
        values = descriptions[item]
        if values["marketable"] == 1:
            temp = {
                    "quantity": 0,
                    "name" : values["market_hash_name"],
                    # "name_color" : "#" + values["name_color"],
                    "type": values["type"],
                    "price": 0.00,
                    "total price": 0.00
                }
            inv[item] = temp

    for item in inventory:
        item_key = inventory[item]['classid'] + "_" + inventory[item]['instanceid']
        try:
            inv[item_key]['quantity'] += 1
        except:
            pass

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["quantity"], reverse=True))
    return inv

def inv_update(inv: dict):
    total = 0.00
    print("aaa")
    for item in inv:
        while True:
            try:
                price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={inv[item]["name"]}'
                price_url2 = f'https://steamcommunity.com/market/pricehistory/?currency=3&appid=730&market_hash_name={inv[item]["name"]}'
                print(price_url)
                response = requests.get(price_url, headers=HEADERS)
                price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))
                quantity = inv[item]["quantity"]
                total_price = round(quantity * price,2)
                
                inv[item]["price"] = price
                inv[item]["total price"] = total_price
                
                total += total_price
                print(f"{total_price}€", inv[item]["name"])
                break
            except TypeError as e:
                if(response.text == "null"):
                    raise e
                print(f"Total till now: {total}€")
                print(price_url)
                with alive_bar(600) as bar:
                    for _ in range(600):
                        time.sleep(0.1)
                        bar()
            except (KeyError, ValueError) as e:
                print(price_url)
                print(e)
                with alive_bar(10) as bar:
                    for _ in range(10):
                        time.sleep(0.1)
                        bar()

    inv = dict(sorted(inv.items(), key=lambda item: item[1]["total price"], reverse=True))
    return inv

def inv_to_graph(inv: dict):
    #TODO print pizza graph where each slice is the price of each item/total price
    
    names = [inv[i]["name"] for i in inv]
    prices = [inv[i]["total price"] for i in inv]
    
    # Create the pie chart using matplotlib
    plt.pie(prices, labels=None, autopct='%1.1f%%')
    plt.title("Item Prices")

    # Add a legend to display the labels outside of the chart
    plt.legend(names, loc="center left", bbox_to_anchor=(1, 0.5))

    plt.show()

def inv_get_total_price(inv: dict):
    total = 0.00
    for i in inv:
        total += inv[i]["total price"]
    total = round(total, 2)
    print(f"total: {total}")
    return total

def load_inv(STEAMID: str):
    try:
        inventory, descriptions = url_to_json(URL)
        inv = json_to_inv(inventory, descriptions)
        print("aaaa")
        inv = inv_update(inv)
        save_inv(STEAMID, inv)
        return inv
    except Exception as e:
        print(e)
        return debug.load_last_save(STEAMID)
        


def main():
    os.system("clear")
    tmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    inv = load_inv(STEAMID)
    print(inv)
    inv_get_total_price(inv)
        

    # debug.save_temp(STEAMID, inv)
    
    # inv = inv_import()
    # inv_to_graph(inv)
    # print(inv)

if __name__ == "__main__":

    main()

