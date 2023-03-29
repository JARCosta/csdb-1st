

users = [
    {"name": "Navi", "steamid": "76561198185395854"},
    {"name": "Jar", "steamid": "76561198285623099"},
    {"name": "Pulga", "steamid": "76561198201367491"}
]

dic = {
    "76561198285623099": {"name": "Jar"},
    "76561198185395854": {"name": "Navi"},
    "76561198201367491": {"name": "Pulga"}
}

def add_user(name: str, steamid: str):
    users.append({name,steamid})

def get_users():
    return users

def get_ids():
    return [user["steamid"] for user in users]
