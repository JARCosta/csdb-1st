

steam_profiles = [{"name": "Navi", "steamid": "76561198185395854"}, {"name": "Jar", "steamid": "76561198285623099"}, {"name": "Pulga", "steamid": "76561198201367491"}]

def add_steam_profile(name: str, steamid: str):
    steam_profiles.append({"name": name, "steamid": steamid})

def get_steam_profiles():
    return steam_profiles

def get_steam_ids():
    return [profile["steamid"] for profile in steam_profiles]