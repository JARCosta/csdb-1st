import json


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://steamcommunity.com/',
    'Connection': 'keep-alive',
    # TODO in server: get cookies from browser
    'Cookie':'''sessionid=e02317942bd01b0cc73283e8; cookieSettings={"version":1,"preference_state":2,"content_customization":null,"valve_analytics":null,"third_party_analytics":null,"third_party_content":null,"utm_enabled":true}; browserid=2825485845585510381; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":0,"time_checked":1679780044}; strInventoryLastContext=730_2; timezoneOffset=3600,0; steamCountry=PT|7622fb70dbc7c719ac7f7e9a46043d42; steamLoginSecure=76561198285623099||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQyMl8yMjQ3RjZFM19ERTFDOSIsICJzdWIiOiAiNzY1NjExOTgyODU2MjMwOTkiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MDIxMDcyMCwgIm5iZiI6IDE2NzE0ODMyNjAsICJpYXQiOiAxNjgwMTIzMjYwLCAianRpIjogIjBEMjdfMjI0RDFEQzRfMDZGOTUiLCAib2F0IjogMTY3OTc4MDAwOSwgInJ0X2V4cCI6IDE2OTc4Mzc0MDMsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NS45My4yNDIuMTQ0IiwgImlwX2NvbmZpcm1lciI6ICI5NS45My4yNDIuMTQ0IiB9.uUqhjQ0y1gcgEDLxF_NAHrSg8VJpDkS7gnBgT-a0gi2jv8tx8YbA3QnARfjUy0BSslUq00_MkyvXj2IK8KL2Bg'''
}

def get_db_connection_string():
    DB_FILE = open("server/utils/config.json")

    DB_INFO = json.load(DB_FILE)
    DB_FILE.close()

    DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
        DB_INFO["DB_HOST"],
        DB_INFO["DB_DATABASE"],
        DB_INFO["DB_USER"],
        DB_INFO["DB_PASSWORD"],
    )
    return DB_CONNECTION_STRING