import json

def is_mod(bot, user):
    guild = bot.get_guild(bot.guild)
    role = guild.get_role(bot.mod_role)
    member = guild.get_member(user.id)
    if role in member.roles:
        return True
    else:
        return False

def is_blacklisted(user):
    with open("blacklist.json", "r") as f:
        blacklist = json.load(f)
    try:
        blacklist[str(user.id)]
    except KeyError:
        return False
    else:
        return True