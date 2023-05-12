import requests
res= requests.get('https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id=35650&page_num=1&_=1657808768032').json()

for price in res['data']['items']:
    print(price['price'])
