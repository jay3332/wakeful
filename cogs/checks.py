import discord
import pwd
import os
from discord.ext import commands
from utils.checks import is_mod


class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_check(self.is_blacklisted)
        bot.add_check(self.maintainance)
        bot.add_check(self.disabled)
        bot.add_check(self.local)

    async def local(self, ctx):
        name = pwd.getpwuid(os.getuid())[0]
        if ctx.author.id == self.bot.ownersid:
            return True
        
        if name == "pi":
            return True
        
        await ctx.send("no you no stop no")
        return False

    async def is_blacklisted(self, ctx):
        query = await ctx.bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", ctx.author.id)
        if query is None:
            return True # isn't blacklisted

        return False # is blacklisted
        
    async def maintainance(self, ctx):
        if ctx.bot.maintainance is True:
            if await ctx.bot.is_owner(ctx.author):
                return True
            await ctx.reply("The bot is currently under maintainance, please wait", mention_author=False)
            return False
        return True

    async def disabled(self, ctx):
        if ctx.guild is None:
            return True
        
        res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
        try:
            commands = res["commands"]
        except (KeyError, TypeError):
            success = False
        else:
            success = True

        if success:
            command_name = ctx.command.qualfied_name if not isinstance(ctx.command, commands.Group) else ctx.command.name
            commands = commands.split(",")
            if (
                command_name in commands
                and not is_mod(self, ctx.author)
            ):
                em = discord.Embed(description="This command has been disabled by the server administrators", color=self.color)
                await ctx.send(embed=em)
                return False
            return True
        return True


def setup(bot):
    bot.add_cog(Checks(bot))
