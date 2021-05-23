import discord, string, random, asyncio, json
from discord.ext import commands
from gtts import gTTS
from utils.configs import color

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ban(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason != None:
                reason = reason + " - requested by {ctx.author} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"requested by {ctx.author} ({ctx.author.id})"))
            em=discord.Embed(description=f"{member} has been successfully banned", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"you moderate with that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def kick(self, ctx, member : discord.Member, *, reason : str = None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason != None:
                reason = reason + " - requested by {ctx.author} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason != None else f"requested by {ctx.author} ({ctx.author.id})"))
            em=discord.Embed(description=f"{member} has been successfully kicked", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"you moderate people with that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=["clear"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def purge(self, ctx, amount : int = 10):
        if not amount > 100:
            e = await ctx.channel.purge(limit=amount)
            em=discord.Embed(description=f"ive successfully purged `{len(e)}` messages", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=em)
            await asyncio.sleep(2)
            await msg.delete()
        else:
            em=discord.Embed(description=f"the maximum amount you can purge is `100`", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nuke(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        em=discord.Embed(description="are you sure you want to do this? this will delete all pins & messages", color=color())
        msg = await ctx.send(embed=em)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message == msg)
        if str(reaction.emoji) == "✅":
            new = await channel.clone()
            await channel.delete()
            em=discord.Embed(description="this channel has been nuked", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
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
            em=discord.Embed(description=f"successfully changed {member}'s nickname to `{nickname}`", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"you moderate people with that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

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
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"you moderate people with that have a higher role position than you", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel = None):
        if channel != None:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            em=discord.Embed(description=f"successfully locked {channel.mention}", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            em=discord.Embed(description=f"this channel has been locked", color=color())
            em.set_footer(text=f"locked by {ctx.author}", icon_url=ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            em=discord.Embed(description=f"successfully locked {ctx.channel.mention}", color=color())
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel = None):
        if channel != None:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            em=discord.Embed(description=f"successfully unlocked {channel.mention}", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            em=discord.Embed(description=f"this channel has been unlocked", color=color())
            em.set_footer(text=f"unlocked by {ctx.author}", icon_url=ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            em=discord.Embed(description=f"successfully unlocked {ctx.channel.mention}", color=color())
            await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix : str = "w,"):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes,f, indent=4)

def setup(bot):
    bot.add_cog(moderation(bot))