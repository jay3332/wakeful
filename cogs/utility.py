import discord, datetime, async_cse, psutil, humanize, os, sys, inspect, mystbin, googletrans, asyncio, aiohttp, random, time, asyncdagpi
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from utils.configs import color
from utils.get import *
from jishaku.functools import executor_function

@executor_function
def do_translate(output, text):
    """
    You have to install googletrans==3.1.0a0 for it to work, as the dev somehow broke it and it doesn't work else
    """
    translator = googletrans.Translator()
    translation = translator.translate(str(text), dest=str(output))
    return translation

google = async_cse.Search(get_config("GOOGLE"))
mystbinn = mystbin.Client()
dagpi = asyncdagpi.Client(get_config("DAGPI"))

class utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mem=[]
        if message.guild:
            for m in message.guild.members:
                if not m.bot:
                    mem.append(m)
            if "@someone" in message.content:
                if message.author.guild_permissions.mention_everyone:
                    await message.channel.send(random.choice(mem).mention)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pypi(self, ctx, package):
        try:
            res = await self.bot.session.get(f"https://pypi.org/pypi/{package}/json")
            json = await res.json()
            name = json["info"]["name"] + " " + json["info"]["version"]
            author = json["info"]["author"] or "None"
            author_email = json["info"]["author_email"] or "None"
            url = json["info"]["project_url"] or "None"
            description = json["info"]["summary"] or "None"
            author = json["info"]["author"] or "None"
            license_ = json["info"]["license"] or "None"
            try:
                documentation = json["info"]["project_urls"]["Documentation"] or "None"
            except:
                documentation = "None"
            try:
                website = json["info"]["project_urls"]["Homepage"] or "None"
            except:
                website = "None"
            keywords = json["info"]["keywords"] or "None"
            em=discord.Embed(
                title=name,
                description=f"{description}\n**author**: {author}\n**author email**: {author_email}\n\n**website**: {website}\n**documentation**: {documentation}\n**keywords**: {keywords}\n**license**: {license_}",
                url=url,
                color=color()
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/381963689470984203/814267252437942272/pypi.png")
            await ctx.send(embed=em)
        except aiohttp.ContentTypeError:
            em=discord.Embed(description=f"this package wasn't found", color=color())
            await ctx.send(embed=em)

    @commands.command(aliases=["g"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, term):
        async with ctx.typing():
            if ctx.channel.is_nsfw():
                safe_search_setting=False
                safe_search="disabled"
            else:
                safe_search_setting=True
                safe_search="enabled"
            value=0
            results = await google.search(str(term), safesearch=safe_search_setting)
            em=discord.Embed(
                title=f"results for: `{term}`",
                timestamp=datetime.datetime.utcnow(),
                color=color()
            ).set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} • safe-search: {safe_search}", icon_url=ctx.author.avatar_url)
            for result in results:
                if not value > 4:
                    epic = results[int(value)]
                    em.add_field(
                        name=f" \uFEFF",
                        value=f"**[{str(epic.title)}]({str(epic.url)})**\n{str(epic.description)}\n",
                        inline=False
                    )
                    value+=1
        await ctx.send(embed=em)

    @commands.command(aliases=["trans", "tr"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, output : str, *, text : str):
        async with ctx.typing():
            translation = await do_translate(output, text)
            em = discord.Embed(color=color())
            em.add_field(name=f"input [{translation.src.upper()}]", value=f"```{text}```", inline=False)
            em.add_field(name=f"output [{translation.dest.upper()}]", value=f"```{translation.text}```", inline=False)
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=["guildav", "servericon", "serverav"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serveravatar(self, ctx, member : discord.Member = None):
        async with ctx.typing():
            avatar_png = ctx.guild.icon_url_as(format="png")
            avatar_jpg = ctx.guild.icon_url_as(format="jpg")
            avatar_jpeg = ctx.guild.icon_url_as(format="jpeg")
            avatar_webp = ctx.guild.icon_url_as(format="webp")
            if ctx.guild.is_icon_animated():
                avatar_gif = ctx.guild.icon_url_as(format="gif")
            if ctx.guild.is_icon_animated():
                embed=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color(), timestamp=datetime.datetime.utcnow())
            else:
                embed=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=ctx.guild.icon_url)
            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["si", "guildinfo", "gi"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        online = 0
        dnd = 0
        idle = 0
        offline = 0
        bots = 0
        if ctx.guild.description == None:
            description=""
        else:
            description = ctx.guild.description
        for member in ctx.guild.members:
            if member.bot:
                bots+=1
            elif member.raw_status == "online":
                online += 1
            elif member.raw_status == "dnd":
                dnd += 1
            elif member.raw_status == "offline":
                offline += 1
            elif member.raw_status == "idle":
                idle += 1
        created_at = ctx.guild.created_at.strftime("20%y/%m/%d at %H:%M:%S")
        em=discord.Embed(
            title=ctx.guild.name,
            description=f"{description}",
            timestamp=datetime.datetime.utcnow(),
            color=color()
        ).set_image(url=ctx.guild.banner_url).set_thumbnail(url=ctx.guild.icon_url)
        em.add_field(
            name="members",
            value=f"online: `{online}`\ndnd: `{dnd}`\nidle: `{idle}`\noffline: `{offline}`\nbots: `{bots}`",
            inline=True
        )
        try:
            booster_role = ctx.guild.premium_subscriber_role.mention or "none"
        except AttributeError:
            booster_role = "none"
        em.add_field(
            name="boosts",
            value=f"- amount: `{ctx.guild.premium_subscription_count}`\n- role: {booster_role}",
            inline=True
        )
        em.add_field(
            name="channels",
            value=f"- all `{len(ctx.guild.channels)}`\n- text: `{len(ctx.guild.text_channels)}`\n- voice: `{len(ctx.guild.voice_channels)}`",
            inline=True
        )
        em.add_field(
            name="other",
            value=f"- owner: {ctx.guild.owner.mention}\n- roles: `{len(ctx.guild.roles)}`\n- region: `{ctx.guild.region}`\n- created at: `{created_at}` ({humanize.naturaltime(ctx.guild.created_at)})",
            inline=True
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["ui", "whois"], description="A command to get information about the given member", usage="[@member]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        #-----------------------------------------------------------
        if not "offline" == str(member.mobile_status):
            mobile_status = self.bot.greenTick
        else:
            mobile_status = self.bot.redTick
        #-----------------------------------------------------------
        if not "offline" == str(member.web_status):
            web_status = self.bot.greenTick
        else:
            web_status = self.bot.redTick
        #-----------------------------------------------------------
        if not "offline" == str(member.desktop_status):
            desktop_status = self.bot.greenTick
        else:
            desktop_status = self.bot.redTick
        #-----------------------------------------------------------
        if member.id == 797044260196319282:
            bot_owner = self.bot.greenTick
        else:
            bot_owner = self.bot.redTick
        #-----------------------------------------------------------
        if member.id == ctx.guild.owner_id:
            guild_owner = self.bot.greenTick
        else:
            guild_owner = self.bot.redTick
        #-----------------------------------------------------------
        if member.bot == True:
            member_bot = self.bot.greenTick
        else:
            member_bot = self.bot.redTick
        #-----------------------------------------------------------    
        created_at = member.created_at.strftime("20%y/%m/%d at %H:%M:%S")
        joined_at = member.joined_at.strftime("20%y/%m/%d at %H:%M:%S")
        em=discord.Embed(
            title=member.name + "#" + member.discriminator,
            timestamp=datetime.datetime.utcnow(),
            color=color()
        )
        em.add_field(
            name="info",
            value=f"- name: `{member.name}`\n- tag: `{member.discriminator}`\n- nickname: `{member.display_name}`\n- mention: {member.mention}\n- id: `{member.id}`\n- status: `{member.raw_status}`\n- bot: {member_bot}\n- mobile: {mobile_status}\n- web: {web_status}\n- desktop: {desktop_status}\n- created at: `{created_at}` ({humanize.naturaltime(member.created_at)})\n- avatar: [click here]({member.avatar_url})",
            inline=True
        )
        if member.top_role.name == "@everyone":
            top_role="none"
        else:
            top_role=member.top_role.mention
        em.add_field(
            name="guild",
            value=f"- owner: {guild_owner}\n- roles: `{len(member.roles)}`\n- top role: {top_role}\n- joined at: `{joined_at}` ({humanize.naturaltime(member.joined_at)})",
            inline=False
        )
        if ctx.message.content.endswith("--roles"):
            em.add_field(
                name=f"roles ({len([e for e in ctx.author.roles if not e.name == '@everyone'])})",
                value=", ".join(f"`{e.name}`" for e in reversed(ctx.author.roles) if not e.name == "@everyone"),
                inline=False
            )
        if member.bot:
            try:
                mutual_guilds=len(member.mutual_guilds)
            except AttributeError:
                mutual_guilds=len(self.bot.guilds)
            em.add_field(
                name="other",
                value=f"- bot owner: {bot_owner}\n- mutual guilds: `{mutual_guilds}`",
                inline=False
            )
        else:
            em.add_field(
                name="other",
                value=f"- mutual guilds: `{len(member.mutual_guilds)}`",
                inline=False
            )
        em.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def suggest(self, ctx):
        cs = self.bot.session
        em=discord.Embed(description=f"please now enter your suggestion below:", color=color())
        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=em)
        try:
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.channel == ctx.channel and msg.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            em=discord.Embed(description="you took too long to respond, now ignoring next messages", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=em)
        else:
            if suggestion.content.lower() != "cancel":
                webhook = Webhook.from_url(str(self.bot.suggestions), adapter=AsyncWebhookAdapter(cs))
                em=discord.Embed(description=f"```{suggestion.content}```", color=color())
                em.set_footer(text=f"suggestion by {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await webhook.send(embed=em)
                await suggestion.add_reaction("✅")
                em=discord.Embed(description="your suggestion has been sent to the admins\nnote: abuse may get you blacklisted", color=color())
                em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await msg.edit(embed=em)
            else:
                await msg.delete()



    @commands.command(aliases=["src"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def source(self, ctx, command_name : str = None):
        if command_name == None:
            em=discord.Embed(description=f"my source code can be found [here]({self.bot.github})", color=color())
            await ctx.send(embed=em)
        else:
            command = self.bot.get_command(command_name)
            if not command:
                em=discord.Embed(description=f"could not find command `{command_name}`", color=color())
                await ctx.send(embed=em)
            else:
                try:
                    source_lines, _ = inspect.getsourcelines(command.callback)
                except (TypeError, OSError):
                    em=discord.Embed(description=f"could retrieve source for `{command_name}`", color=color())
                    await ctx.send(embed=em)
                else:
                    source_lines = ''.join(source_lines).split('\n')
                    src = "\n".join(line for line in source_lines).replace("`", "'")
                    em=discord.Embed(title=f"{command.name} source", description=f"note: most of the \" ' \" stand for a \" ` \"\n\n```py\n{src}```", color=color(), timestamp=datetime.datetime.utcnow())
                    em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    try:
                        await ctx.author.send(embed=em)
                    except discord.HTTPException:
                        async with ctx.author.typing():
                            post = await mystbinn.post(src)
                            em=discord.Embed(description=f"note: most of the \" ' \" stand for a \" ` \"\nthe output was too long so it got uploaded to [mystbin]({post})", color=color(), timestamp=datetime.datetime.utcnow())
                            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.author.send(embed=em)
                    await ctx.message.add_reaction("✅")

    @commands.command(aliases=["icon", "av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member : discord.Member = None):
        async with ctx.typing():
            if not member:
                member = ctx.author
            avatar_png = member.avatar_url_as(format="png")
            avatar_jpg = member.avatar_url_as(format="jpg")
            avatar_jpeg = member.avatar_url_as(format="jpeg")
            avatar_webp = member.avatar_url_as(format="webp")
            if member.is_avatar_animated():
                avatar_gif = member.avatar_url_as(format="gif")
            if member.is_avatar_animated():
                embed=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color(), timestamp=datetime.datetime.utcnow())
            else:
                embed=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=member.avatar_url)
            embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["lc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lettercount(self, ctx, *, text):
        em=discord.Embed(description=f"your text is {len(text)} letters long", color=color())
        await ctx.send(embed=em)

    @commands.command(aliases=["wc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wordcount(self, ctx, *, text):
        text_list = text.split(" ")
        em=discord.Embed(description=f"your text is {len(text_list)} words long", color=color())
        await ctx.send(embed=em)

    @commands.command(aliases=["botinfo", "about", "bi"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        operating_system=None
        if os.name == "nt":
            operating_system = "windows"
        elif os.name == "posix":
            operating_system = "linux"
        async with ctx.typing():
            process = psutil.Process()
            version = sys.version_info
            embed = discord.Embed(color=color())
            delta_uptime = datetime.datetime.utcnow() - self.bot.uptime
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            channels = {"all": 0, "category": 0, "text": 0, "voice": 0, "stage": 0}
            for guild in self.bot.guilds:
                for channel in guild.channels:
                    channels["all"] += 1
                    if isinstance(channel, discord.CategoryChannel):
                        channels["category"] +=1
                    elif isinstance(channel, discord.TextChannel):
                        channels["text"] += 1
                    elif isinstance(channel, discord.VoiceChannel):
                        channels["voice"] += 1
                    elif isinstance(channel, discord.StageChannel):
                        channels["stage"] += 1
                    else:
                        print(channel.__class__)
            embed.add_field(name="system", value=f"""
- **os**: `{operating_system}`
- **cpu**: `{process.cpu_percent()}`%
- **memory**: `{humanize.naturalsize(process.memory_full_info().rss).lower()}`
- **process**: `{process.pid}`
- **threads**: `{process.num_threads()}`
- **language**: `python`
- **python version**: `{version[0]}.{version[1]}.{version[2]}`
- **discord.py version**: `{discord.__version__}`""", inline=True)
            embed.add_field(name="bot", value=f"""
- **guilds**: `{len(self.bot.guilds)}`
- **users**: `{len(self.bot.users)}`
- **channels**: `{channels["all"]}`:
    - **categories**: `{channels["category"]}`
    - **text**: `{channels["text"]}`
    - **voice**: `{channels["voice"]}`
    - **stage**: `{channels["stage"]}`
- **commands**: `{len(self.bot.commands)}`
- **commands executed**: `{self.bot.cmdsSinceRestart}`
- **cogs**: `{len(self.bot.cogs)}`
- **uptime**: `{days}d {hours}h {minutes}m {seconds}s`
- [source]({self.bot.github})
- [invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)""", inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["rp", "activity", "richpresence", "status"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def presence(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s activities", color=color(), timestamp=datetime.datetime.utcnow())
        for activity in member.activities:
            if isinstance(activity, discord.activity.Spotify):
                artists = ", ".join(artist for artist in activity.artists)
                duration = activity.duration
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                em.add_field(
                    name="Spotify",
                    value=f"""
title: `{activity.title}`
artists: `{artists}`
album: `{activity.album}`
album cover: [url]({activity.album_cover_url})
duration: `{hours}`h `{minutes}`m `{seconds}`s
""",
                    inline=False
                )
            elif isinstance(activity, discord.activity.CustomActivity):
                if activity.emoji != None:
                    emoji = f"[url]({activity.emoji.url})"
                    emojiName = f"`{activity.emoji.name}`"
                else:
                    emoji = "`None`"
                    emojiName = "`None`"
                em.add_field(
                    name="Custom",
                    value=f"""
text: `{activity.name}`
emoji: {emoji}
emoji name: {emojiName}
""",
                    inline=False
                )
            elif isinstance(activity, discord.activity.Game):
                em.add_field(
                    name="Game",
                    value=f"name: `{activity.name}`",
                    inline=False
                )
            elif isinstance(activity, discord.activity.Streaming):
                em.add_field(
                    name="Stream",
                    value=f"""
title: `{activity.name}`
platform: `{activity.platform}`
url: [{activity.url.split("/")[3]}]({activity.url})
""",
                    inline=False
                )
            else:
                em.add_field(
                    name="Unknown",
                    value=f"name: `{activity.name}`",
                    inline=False
                )
        em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def snipe(self, ctx):
        try:
            msg = self.bot.message_cache[ctx.guild.id][ctx.channel.id]
        except KeyError:
            em=discord.Embed(description=f"there's no message to snipe", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"`{msg.content}`", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_author(name=f"{msg.author} ({msg.author.id})", icon_url=msg.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=["rtfd"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rtfm(self, ctx, query):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location=https://discordpy.readthedocs.io/en/latest&show-labels=false&label-labels=false")
            res = await res.json()
            nodes = res["nodes"]
        if nodes != {}:
            em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color())
            em.set_footer(text=f"powered by idevision.net • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em=discord.Embed(description=f"no results found for `{query}`", color=color())
            em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, command : str = None):
        if command == None:
            raw_cogs=[]
            for cog in self.bot.cogs:
                raw_cogs.append(cog)
            cog_objects=[]
            for cog in raw_cogs:
                cog_objects.append(self.bot.get_cog(str(cog)))
            names = f"\n".join(cog.qualified_name for cog in cog_objects)
            commandse = []
            for cog in cog_objects:
                for command in cog.walk_commands():
                    commandse.append(command.name)
            commands=", ".join(command for command in commandse)
            em=discord.Embed(
                description=f"type `{ctx.prefix}help [command]` for more information about a command.",
                timestamp=datetime.datetime.utcnow(),
                color=color()
            ).set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            for cog in cog_objects:
                if cog.get_commands():
                    if not cog.qualified_name == "Jishaku":
                        if not cog.qualified_name == "Developer":
                            listts=[]
                            for command in cog.walk_commands():
                                if not command.hidden:
                                    if not command.parent:
                                        listts.append(f"`{command.name}`")
                            em.add_field(
                                name=f"{cog.qualified_name} ({len(cog.get_commands())})",
                                value="> " + ", ".join(command for command in listts),
                                inline=False
                            )
            await ctx.send(embed=em)
        else:
            if self.bot.get_command(str(command)):
                given_command = self.bot.get_command(str(command))
                if not given_command.hidden == True:
                    can_run_check = await self.bot.can_run(given_command)
                    #-------------------------------------
                    if can_run_check == True:
                        can_run = self.bot.greenTick
                    elif can_run_check == False:
                        can_run = self.bot.redTick
                    #-------------------------------------
                    try:
                        command_subcommands = "> " + ", ".join(f"`{command.name}`" for command in given_command.commands)
                    except:
                        command_subcommands = "none"
                    #-------------------------------------
                    if given_command.enabled == True:
                        command_enabled = self.bot.greenTick
                    elif given_command.enabled == False:
                        command_enabled = self.bot.redTick
                    #-------------------------------------
                    if given_command.usage:
                        command_usage = given_command.usage
                    else:
                        command_usage = " ".join(f"<{e}>" for e in list(given_command.params) if not e in ["self", "ctx"])
                    #-------------------------------------
                    if given_command.parent:
                        command_parent = given_command.parent
                    else:
                        command_parent = "none"
                    #-------------------------------------
                    em=discord.Embed(
                        title=given_command.name,
                        timestamp=datetime.datetime.utcnow(),
                        description=given_command.description,
                        color=color()
                    ).set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    em.add_field(name="usage", value=f"{ctx.prefix}{command} {command_usage}", inline=False)
                    if given_command.aliases:
                        em.add_field(name=f"aliases [{len(given_command.aliases)}]", value="> " + ", ".join(f"`{alias}`" for alias in given_command.aliases), inline=False)
                    else:
                        em.add_field(name="aliases [0]", value="none", inline=False)
                    try:
                        em.add_field(name=f"subcommands [{len(given_command.commands)}]", value=command_subcommands, inline=False)
                    except AttributeError:
                        em.add_field(name=f"subcommands [0]", value=command_subcommands, inline=False)
                    em.add_field(name="category", value=given_command.cog_name, inline=False)
                    await ctx.send(embed=em)
                else:
                    em=discord.Embed(description=f"this command does not exist", color=color())
                    await ctx.send(embed=em)
            else:
                em=discord.Embed(description=f"this command does not exist", color=color())
                await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        embed=discord.Embed(color=color())
        dagpi_ping = round(await dagpi.image_ping(), 3) * 1000
        embed.add_field(name="latency", value=f"""
- **typing**: `pinging`
- **bot**: `{round(self.bot.latency*1000)}`ms
- **database**: `pinging`
- **dagpi**: `{dagpi_ping}`ms""", inline=False)
        start=time.perf_counter()
        msg = await ctx.send(embed=embed)
        end=time.perf_counter()
        final=end-start
        api_latency = round(final*1000)
        em=discord.Embed(color=color())
        poststart = time.perf_counter()
        await self.bot.db.fetch("SELECT 1")
        postduration = (time.perf_counter() - poststart) * 1000
        db_ping = round(postduration, 1)
        em.add_field(name="latency", value=f"""
- **typing**: `{api_latency}`ms
- **bot**: `{round(self.bot.latency*1000)}`ms
- **database**: `{db_ping}`ms
- **dagpi**: `{dagpi_ping}`ms""", inline=False)
        await msg.edit(embed=em)

    @commands.command()
    async def afk(self, ctx, *, reason : str = None):
        if reason is None:
            msg = f"okay, i've marked you as afk"
        else:
            msg = f"okay, i've marked you as afk for `{reason}`"
        em=discord.Embed(description=msg, color=color())
        await ctx.send(embed=em)
        await asyncio.sleep(3)
        self.bot.afks[ctx.author.id] = {"reason": reason}

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id in list(self.bot.afks):
            self.bot.afks.pop(msg.author.id)
            em=discord.Embed(description=f"welcome back, {msg.author.mention}, i've unmarked you as afk", color=color())
            await msg.channel.send(embed=em)
        for user in list(self.bot.afks):
            data = self.bot.afks[user]
            obj = self.bot.get_user(user)
            if f"<@!{user}>" in msg.content or f"<@{user}>" in msg.content:
                if data["reason"] is None:
                    mseg = f"hey! {obj.name} is currently marked as afk"
                else:
                    mseg = f"hey! {obj.name} is currently marked as afk for `{data['reason']}`"
                em=discord.Embed(description=mseg, color=color())
                await msg.reply(embed=em)

def setup(bot):
    bot.add_cog(utility(bot))