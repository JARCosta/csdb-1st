import json
from time import sleep
import requests

steamid = "76561198285623099"

url = f"https://steamcommunity.com/profiles/{steamid}/inventory/json/730/2"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://steamcommunity.com/',
    'Connection': 'keep-alive',
    'Cookie':'sessionid=e02317942bd01b0cc73283e8; timezoneOffset=0,0; cookieSettings={"version":1,"preference_state":2,"content_customization":null,"valve_analytics":null,"third_party_analytics":null,"third_party_content":null,"utm_enabled":true}; steamCountry=PT|7dce34e55c2187275d8dda742200b938; steamLoginSecure=76561198285623099||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQyMl8yMjQ3RjZFM19ERTFDOSIsICJzdWIiOiAiNzY1NjExOTgyODU2MjMwOTkiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY3OTg2ODIwOSwgIm5iZiI6IDE2NzExNDAwMDksICJpYXQiOiAxNjc5NzgwMDA5LCAianRpIjogIjBEMjdfMjI0N0Y3MEFfREEyMDIiLCAib2F0IjogMTY3OTc4MDAwOSwgInJ0X2V4cCI6IDE2OTc4Mzc0MDMsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NS45My4yNDIuMTQ0IiwgImlwX2NvbmZpcm1lciI6ICI5NS45My4yNDIuMTQ0IiB9.2H7Bjcn5I6wK12dHdNi-fKDM7J87xfBr-lkYMUfeBBbzJxtMm21xj3IiMLVHTa_XglX1ygjJSyYK7IztbYKNBg; browserid=2825485845585510381; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":0,"time_checked":1679780044}; strInventoryLastContext=730_2'
}


def get_els():
    [print(i) for i in json.loads(requests.get(url, headers=headers).content)]


def import_items():
    response = requests.get(url, headers=headers)
    descriptions = json.loads(response.content)['rgInventory']
    file = open("qnts.json",'w',encoding='utf-8')
    file.write(json.dumps(descriptions, indent=4))
    file.close()


def import_descs():
    response = requests.get(url, headers=headers)
    descriptions = json.loads(response.content)['rgDescriptions']
    
    file = open("descs.json",'w',encoding='utf-8')
    file.write(json.dumps(descriptions, indent=4))
    file.close()


def filter(dic:dict, func):
    # filter the dict by the function
    return {k: v for k, v in dic.items() if func(v)}


def get_qnts_by_items():
    
    dic = {}

    descs = open("descs.json",'r',encoding='utf-8')
    descs = json.load(descs)
    for i in descs:
        values = descs[i]
        if values["marketable"] == 1:
            temp = {
                "quantity": 0,
                "name" : values["market_hash_name"],
                # "name_color" : "#" + values["name_color"],
                "type": values["type"],
                "price": 0.00,
                "total price": 0.00
            }
            dic[i] = temp
    

    qnts = open("qnts.json",'r',encoding='utf-8')
    qnts = json.load(qnts)
    for i in qnts:
        values = qnts[i]
        try:
            dic[values["classid"] + "_"+ values["instanceid"]]["quantity"] += 1
        except:
            pass


    dic = dict(sorted(dic.items(), key=lambda item: item[1]["quantity"], reverse=True))

    total = 0.0
    loop = 0
    for i in dic:
        while True:
            try:
                price_url = f'https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name={dic[i]["name"]}'
                response = requests.get(price_url, headers=headers)
                price = float(json.loads(response.content)['lowest_price'][:-1].replace(",","."))
                quantity = dic[i]["quantity"]
                total_price = round(quantity * price,2)
                
                dic[i]["price"] = price
                dic[i]["total price"] = total_price
                
                total += total_price
                
                print(str(total_price)+"€", dic[i]["name"])
                
                break
            except Exception as e:
                print(response.content)
                print(e)
                sleep(60)
        loop -= 1
        if loop == 0:
            break

    dic = dict(sorted(dic.items(), key=lambda item: item[1]["total price"], reverse=True))

    print("total" , round(total, 2) , "€")

    file = open("inv.json",'w',encoding='utf-8')
    file.write(json.dumps(dic, indent=4))
    file.write('\n"total": ' + str(total) + "€\n")
    file.close()


# get_els()

# import_items()
# import_descs()

get_qnts_by_items()


