import json

def is_mod(bot, user):
    guild = bot.get_guild(bot.guild)
    role = guild.get_role(bot.mod_role)
    member = guild.get_member(user.id)
    if role in member.roles:
        return True
    else:
        return False

async def is_blacklisted(bot, user):
    try:
        blacklist = await bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", user.id)
        blacklist["user_id"]
        return True
    except:
        return False