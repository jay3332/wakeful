from datetime import datetime
import discord, string, random, asyncio, asyncpg
from discord.ext import commands
from gtts import gTTS
from utils.configs import color

class Moderation(commands.Cog):

    """Moderation commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def disable(self, ctx, command):
        if not command in ["help"]:
            command = self.bot.get_command(command)
            if command is None:
                em=discord.Embed(description=f"This command hasn't been found", color=color())
                await ctx.reply(embed=em, mention_author=False)
            elif command.hidden:
                em=discord.Embed(description=f"This command hasn't been found", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                try:
                    await self.bot.db.execute("INSERT INTO commands (guild, commands) VALUES ($1, $2)", ctx.guild.id, command.name)
                except asyncpg.UniqueViolationError:
                    commands = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                    commands = commands["commands"]
                    commands = commands.split(",")
                    if not command.name in commands:
                        commands.append(command.name)
                        commands = ",".join(cmd for cmd in commands)
                        await self.bot.db.execute("UPDATE commands SET commands = $1 WHERE guild = $2", commands, ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully disabled the `{command.name}` command", color=color())
                        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em=discord.Embed(description=f"That command is already disabled", color=color())
                        await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"I've successfully disabled the `{command.name}` command", color=color())
                    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You are not allowed to disable the `{command}` command", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def enable(self, ctx, command):
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
                if command.name in commands:
                    commands.remove(command.name)
                    commands = ",".join(cmd for cmd in commands)
                    if len(commands) != 1:
                        await self.bot.db.execute("UPDATE commands SET commands = $1 WHERE guild = $2", commands, ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully enabled the `{command.name}` command", color=color())
                        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        await self.bot.db.fetch("DELETE FROM commands WHERE guild = $1", ctx.guild.id)
                        em=discord.Embed(description=f"I've successfully enabled the `{command.name}` command", color=color())
                        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"That command isn't disabled", color=color())
                    await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ban(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason != None:
                reason = reason + " - Requested by {ctx.author} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"requested by {ctx.author} ({ctx.author.id})"))
            em=discord.Embed(description=f"{member} has been successfully banned", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def kick(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason != None:
                reason = reason + " - Requested by {ctx.author} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason != None else f"requested by {ctx.author} ({ctx.author.id})"))
            em=discord.Embed(description=f"{member} has been successfully kicked", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["clear"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def purge(self, ctx, amount : int = 10):
        if not amount > 100:
            e = await ctx.channel.purge(limit=amount)
            em=discord.Embed(description=f"I've successfully purged `{len(e)}` messages", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            msg = await ctx.reply(embed=em, mention_author=False)
            await asyncio.sleep(2)
            await msg.delete()
        else:
            em=discord.Embed(description=f"The maximum amount you can purge is `100`", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nuke(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        em=discord.Embed(description="Are you sure you want to do this? this will delete all pins & messages", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user.guild_permissions.manage_channels and str(reaction.emoji) in ["✅", "❌"] and reaction.message == msg)
        if str(reaction.emoji) == "✅":
            new = await channel.clone()
            await channel.delete()
            em=discord.Embed(description="This channel has been nuked", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await new.send(embed=em)
        elif str(reaction.emoji) == "❌":
            await msg.delete()

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nickname(self, ctx, member : discord.Member, *, nickname : str = ""):
        if ctx.author.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
            em=discord.Embed(description=f"Successfully changed {member}'s nickname to `{nickname}`", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["modnick", "moderatenick", "modnickname"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def moderatenickname(self, ctx, member : discord.Member):
        if ctx.author.top_role.position > member.top_role.position:
            nicks = []
            for m in ctx.guild.members:
                if m.nick:
                    nicks.append(m.nick.lower())
            while True:
                nickname = "moderated nickname "+"".join(random.choice(string.ascii_letters+string.digits) for x in range(5))
                if not nickname in nicks:
                    await member.edit(nick=nickname)
                    break
            em=discord.Embed(description=f"successfully changed {member}'s nickname to `{nickname}`", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"You can't moderate people that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel = None):
        if channel != None:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            em=discord.Embed(description=f"successfully locked {channel.mention}", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
            em=discord.Embed(description=f"this channel has been locked", color=color())
            em.set_footer(text=f"locked by {ctx.author}", icon_url=ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            em=discord.Embed(description=f"successfully locked {ctx.channel.mention}", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel = None):
        if channel != None:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            em=discord.Embed(description=f"successfully unlocked {channel.mention}", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
            em=discord.Embed(description=f"this channel has been unlocked", color=color())
            em.set_footer(text=f"unlocked by {ctx.author}", icon_url=ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            em=discord.Embed(description=f"successfully unlocked {ctx.channel.mention}", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix : str = "w,"):
        try:
            await self.bot.db.execute("INSERT INTO prefixes (guild, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
        except asyncpg.UniqueViolationError:
            await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild = $2", prefix, ctx.guild.id)
        em=discord.Embed(description=f"sucessfully set the prefix for `{ctx.guild.name}` to `{prefix}`", color=color())
        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(Moderation(bot))