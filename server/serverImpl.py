

steam_profiles = [{"name": "NAVi", "steamid": "76561198185395854"}, {"name": "JAR", "steamid": "76561198285623099"}]

def add_steam_profile(name: str, steamid: str):
    steam_profiles.append({"name": name, "steamid": steamid})

def get_steam_profiles():
    return steam_profiles

def get_steam_ids():
    return [profile["steamid"] for profile in steam_profiles]