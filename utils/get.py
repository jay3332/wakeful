import json

def get_config(string : str):
    with open("config.json", "r") as f:
        conf = json.load(f)
    value = conf[string]
    return value

def get_cog(bot, name):
    for cog in bot.cogs:
        cog = bot.get_cog(cog)
        if cog.qualified_name.lower() == name.lower():
            return cog