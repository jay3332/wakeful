import json

def get_config(string : str):
    with open("config.json", "r") as f:
        conf = json.load(f)
    value = conf[string]
    return value

def get_owner(bot):
    owners = list(bot.owner_ids)
    print(owners)
    return owners[0]
