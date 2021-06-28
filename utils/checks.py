
import discord
import typing
from discord.ext import commands

def is_mod(bot: typing.Union[discord.Client, commands.Bot], user: discord.User):
    guild = bot.get_guild(bot.guild)
    role = guild.get_role(bot.mod_role)
    member = guild.get_member(user.id)
    try:
        return role in member.roles
    except:
        return False

def gameRunning(ctx: commands.Context, game: str):
    try:
        ctx.bot.games[game][str(ctx.guild.id)]
    except KeyError:
        return False
    else:
        return True

async def is_blacklisted(bot, user):
    blacklist = await bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", user.id)
    try:
        blacklist["user_id"]
    except KeyError:
        return False
    else:
        return True