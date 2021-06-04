import json

def is_mod(bot, user):
    guild = bot.get_guild(bot.guild)
    role = guild.get_role(bot.mod_role)
    member = guild.get_member(user.id)
    try:
        if role in member.roles:
            return True
        else:
            return False
    except:
        return False

async def is_blacklisted(bot, user):
    blacklist = await bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", user.id)
    try:
        blacklist["user_id"]
    except:
        return False
    else:
        return True