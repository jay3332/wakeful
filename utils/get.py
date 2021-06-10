import json, datetime, discord, typing, aiohttp

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
    
def color():
    return int(get_config("COLOR"), 16)

async def get_pronoun(bot : typing.Union[discord.Client, discord.ext.commands.Bot], member : discord.Member):
    pronouns={
        "hh": "he/him",
        "hi": "he/it",
        "hs": "/he/she",
        "ht": "he/they",
        "ih": "it/him",
        "ii": "it/its",
        "is": "it/she",
        "it": "it/they",
        "shh": "she/he",
        "sh": "she/her",
        "si": "she/it",
        "st": "she/they",
        "th": "they/he",
        "ti": "they/it",
        "ts": "they/she",
        "tt": "they/them",
        "any": "Any",
        "other": "Other",
        "ask": f"Ask",
        "avoid": "No pronoun, use name"
    }
    res = await (await bot.session.get(f"https://pronoundb.org/api/v1/lookup?id={member.id}&platform=discord")).json()
    try:
        code = res["pronouns"]
    except KeyError:
        code = "None"
    return pronouns[code]
