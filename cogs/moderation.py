from datetime import datetime
import discord, string, random, asyncio, asyncpg
from discord.ext import commands
from utils.get import *
from __main__ import get_prefix

class Moderation(commands.Cog):

    """Moderation commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def disable(self, ctx, *, command):
        if not command in ["help"]:
            command = self.bot.get_command(command)
            if command is None:
                em=discord.Embed(description=f"This command hasn't been found", color=color())
                await ctx.reply(embed=em, mention_author=False)
            elif command.hidden:
                em=discord.Embed(description=f"This command hasn't been found", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                command_name = "".join(command.name if command.parent is None else f"{command.parent.name} {command.name}")
                try:
                    await self.bot.db.execute("INSERT INTO commands (guild, commands) VALUES ($1, $2)", ctx.guild.id, command_name)
                except asyncpg.UniqueViolationError:
                    commands = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                    commands = commands["commands"]
                    commands = commands.split(",")
                    if not command_name in commands:
                        commands.append(command_name)
                        commands = ",".join(cmd for cmd in commands)
                        await self.bot.db.execute("UPDATE commands SET commands = $1 WHERE guild = $2", commands, ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully disabled the `{command_name}` command", color=color())
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em=discord.Embed(description=f"That command is already disabled", color=color())
                        await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"I've successfully disabled the `{command_name}` command", color=color())
                    await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You are not allowed to disable the `{command}` command", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def enable(self, ctx, *, command):
        command = self.bot.get_command(command)
        if command is None:
            em=discord.Embed(description=f"This command hasn't been found", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif command.hidden:
            em=discord.Embed(description=f"This command hasn't been found", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
            try:
                res["commands"]
            except TypeError:
                em=discord.Embed(description=f"That command isn't disabled", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                commands = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                commands = commands["commands"]
                commands = commands.split(",")
                command_name = "".join(command.name if command.parent is None else f"{command.parent.name} {command.name}")
                if command_name in commands:
                    commands.remove(command_name)
                    commands = ",".join(cmd for cmd in commands)
                    if len(commands) != 1:
                        await self.bot.db.execute("UPDATE commands SET commands = $1 WHERE guild = $2", commands, ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully enabled the `{command_name}` command", color=color())
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        await self.bot.db.fetch("DELETE FROM commands WHERE guild = $1", ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully enabled the `{command_name}` command", color=color())
                        await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"That command isn't disabled", color=color())
                    await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ban(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.message.add_reaction(self.bot.icons["greentick"])
        else:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def kick(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = reason + f"{reason} - Requested by {ctx.author} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason is not None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.message.add_reaction(self.bot.icons["greentick"])
        else:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["clear"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def purge(self, ctx, amount : int = 10):
        if not amount > 100:
            e = await ctx.channel.purge(limit=amount)
            em=discord.Embed(description=f"I've successfully purged `{len(e)}` messages", color=color())
            await ctx.reply(embed=em, mention_author=False, delete_after=2)
        else:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"The maximum amount you can purge is `100`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nuke(self, ctx, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        em=discord.Embed(description="Are you sure you want to execute this command? This will delete all pins & messages", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)
        await msg.add_reaction(self.bot.icons["greentick"])
        await msg.add_reaction(self.bot.icons["redtick"])
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user.guild_permissions.manage_channels and str(reaction.emoji) in [self.bot.icons['redtick'], self.bot.icons['greentick']] and reaction.message == msg and not user.bot)
        if str(reaction.emoji) == self.bot.icons['greentick']:
            new = await channel.clone()
            await channel.delete()
            em=discord.Embed(description="This channel has been nuked", color=color())
            await new.send(embed=em)
        elif str(reaction.emoji) == self.bot.icons['redtick']:
            await msg.delete()

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nickname(self, ctx, member : discord.Member, *, nickname : str = ""):
        if ctx.author.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
            await ctx.message.add_reaction(self.bot.icons["greentick"])
        else:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["modnick", "moderatenick", "modnickname"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def moderatenickname(self, ctx, member : discord.Member):
        if ctx.author.top_role.position > member.top_role.position:
            nicks = []
            for m in ctx.guild.members:
                if m.nick:
                    nicks.append(m.nick.lower())
            while True:
                nickname = "Moderated Nickname "+"".join(random.choice(string.ascii_letters+string.digits) for x in range(5))
                if not nickname in nicks:
                    await member.edit(nick=nickname)
                    break
            await ctx.message.add_reaction(self.bot.icons["greentick"])
        else:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["prefix"])
    @commands.guild_only()
    async def setprefix(self, ctx, prefix : str = None):
        if prefix is None:
            prefix = await get_prefix(self.bot, ctx.message)
            if ctx.message.guild:
                em=discord.Embed(description=f"The prefix for `{ctx.message.guild.name}` is `{prefix[2]}`", color=color())
                return await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"The prefix for dms is `{prefix[2]}`", color=color())
                return await ctx.reply(embed=em, mention_author=False)

        if not ctx.author.guild_permissions.manage_guild:
            raise commands.MissingPermissions(["manage_guild"])

        if len(prefix) > 10:
            return await ctx.reply("The prefix can't be over 10 characters long", mention_author=False)

        try:
            await self.bot.db.execute("INSERT INTO prefixes (guild, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
        except asyncpg.UniqueViolationError:
            await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild = $2", prefix, ctx.guild.id)
        em=discord.Embed(description=f"I've set the prefix for `{ctx.guild.name}` to `{prefix}`", color=color())
        await ctx.reply(embed=em, mention_author=False)

    

def setup(bot):
    bot.add_cog(Moderation(bot))