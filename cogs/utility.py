import discord, datetime, async_cse, psutil, humanize, os, sys, inspect, mystbin, googletrans, asyncio, aiohttp, random, time, lyricsgenius
import asyncdagpi, hashlib, asyncpg, io, typing, gdshortener, pathlib, textwrap, async_tio, zipfile, aiowiki
import mathjspy, pytube, youtube_dl, re 

from discord.ext import commands
from utils.webhook import Webhook, AsyncWebhookAdapter
from utils.get import *
from utils.paginator import Paginator
from utils.checks import *
from utils.errors import *
from __main__ import get_prefix

from utils.functions import * 
from utils.paginator import *
from jishaku.functools import executor_function
from jishaku.codeblocks import codeblock_converter
from shazamio.api import Shazam

client = Shazam()
google = async_cse.Search(get_config("GOOGLE"))
mystbinn = mystbin.Client()
dagpi = asyncdagpi.Client(get_config("DAGPI"))
isgd = gdshortener.ISGDShortener()
genius = lyricsgenius.Genius(get_config("GENIUS"))

@executor_function
def cleanup(path):
    path.cleanup()

@executor_function
def make():
    directory = tempfile.TemporaryDirectory()
    return directory

@executor_function
def do_translate(output, text):
    """
    You have to install googletrans==3.1.0a0 for it to work, as the dev somehow broke it and it doesn't work else
    """
    translator = googletrans.Translator()
    translation = translator.translate(str(text), dest=str(output))
    return translation

@executor_function
def get_song(song, artist = None):
    return genius.search_song(title=song, artist=artist)

@executor_function
def download_emojis(emojis : tuple):
    file_ = io.BytesIO()
    with zipfile.ZipFile(file_, mode="w", compression=getattr(zipfile, "ZIP_DEFLATED"), compresslevel=9) as zipfile_:
        for a, b in emojis:
            zipfile_.writestr(a, b.getvalue())
    file_.seek(0)
    return discord.File(file_, "emojis.zip")

@executor_function
def download(url):
    try:
        video = pytube.YouTube(str(url))
    except Exception as exc:
        raise NotFound(exc)
    if video.length > 900:
        raise TooLong("The video cannot be longer than 15 minutes.")
    res = video.streams.get_highest_resolution()
    buffer = io.BytesIO()
    download = res.stream_to_buffer(buffer)
    download.seek(0)
    file_ = discord.File(str(download))
    return file_

class Utility(commands.Cog):

    """Useful commands"""

    def __init__(self, bot):
        self.bot = bot
        self.wiki = aiowiki.Wiki.wikipedia("en")
        self.ytdl = youtube_dl.YoutubeDL({"format": "bestaudio/best", "restrictfilenames": True, "noplaylist": True, "nocheckcertificate": True, "ignoreerrors": True, "logtostderr": False, "quiet": True, "no_warnings": True, "default_search": "auto", "source_address": "0.0.0.0"})

    @commands.Cog.listener(name="on_message")
    async def afk_messages(self, msg):
        if msg.author.id in list(self.bot.afks):
            self.bot.afks.pop(msg.author.id)
            em=discord.Embed(description=f"Welcome back, {msg.author.mention}, I've unmarked you as afk", color=color())
            await msg.channel.send(embed=em)
        for user in list(self.bot.afks):
            data = self.bot.afks[user]
            obj = self.bot.get_user(user)
            if f"<@!{user}>" in msg.content or f"<@{user}>" in msg.content:
                if data["reason"] is None:
                    mseg = f"Hey! {obj.name} is currently marked as afk"
                else:
                    mseg = f"Hey! {obj.name} is currently marked as afk for `{data['reason']}`"
                await msg.channel.reply(embed=em, mention_author=False)


    @commands.Cog.listener(name="on_message")
    async def emojj_system(self, msg):
        if msg.author.bot:
            return
        if ";;" in msg.content:
            emojis = msg.content.split(";;")
            emoji_ = emojis[1]
            if emoji_ != "" and not " " in emoji_:
                res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
                try:
                    res["commands"]
                except TypeError:
                    pass
                else:
                    commands = res["commands"]
                    commands = commands.split(",")
                    if len(commands) != 0 and commands != ['']:
                        if "emojis" in commands:
                            return
                        else:
                            pass
                    else:
                        pass
                res = await self.bot.db.fetchrow("SELECT user_id FROM emojis WHERE user_id = $1", msg.author.id)
                try:
                    res["user_id"]
                except TypeError:
                    return
                else:
                    emoji = None
                    for e in self.bot.emojis:
                        if e.name.lower().startswith(emoji_.lower()):
                            emoji = e
                    if emoji is not None:
                        await msg.reply(str(emoji), mention_author=False)

    @commands.command(aliases=["wiki"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wikipedia(self, ctx, *, query):
        query = query.title()
        page = self.wiki.get_page(query)
        if page is None:
            return await ctx.reply(f"I couldn't find a wikipedia page with the query `{query}`", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        title = page.title
        try:
            summary = await page.summary()
        except:
            return await ctx.reply(f"I couldn't find a wikipedia page with the query `{query}`", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        if len(summary) == 0:
            return await ctx.reply(f"I couldn't find a wikipedia page with the query `{query}`", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        url = (await page.urls()).view
        media = await page.media()
        text = WrapText(summary, 2048)
        embeds = []
        for txt in text:
            em=discord.Embed(title=title, description=str(txt), url=url, color=color())
            if len(media) != 0 and media != []:
                em.set_thumbnail(url=random.choice(media))
            embeds.append(em)
        pag = self.bot.paginate(Paginator(embeds, per_page=1))
        await pag.start(ctx)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lyrics(self, ctx, *, song):
        song_name = song.replace(" --txt", "")
        async with ctx.typing():
            res = await get_song(song=song_name)
        if res is None:
            return await ctx.reply(f"I couldn't find a song with the name `{song_name}`", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        if not song.endswith("--txt"):
            text = WrapText(res.lyrics, 2024)
            embeds = []
            for txt in text:
                em=discord.Embed(title=f"{res.title} Lyrics", description=txt, color=color())
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            await ctx.reply(file=await getFile(res.lyrics, filename=f"{res.title}_lyrics"), mention_author=False)
        
    @commands.command(aliases=["content"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def read(self, ctx):
        if not ctx.message.reference:
            em=discord.Embed(description=f"Please reply to the message you want to read", color=color())
            return await ctx.reply(embed=em, mention_author=False)
        if not ctx.message.reference.resolved.attachments:
            em=discord.Embed(description=f"The message you replied to doesn't have any attachments", color=color())
            return await ctx.reply(embed=em, mention_author=False)
        res = (await ctx.message.reference.resolved.attachments[0].read()).decode()
        text = WrapText(res, 2024)
        embeds = []
        filename = ctx.message.reference.resolved.attachments[0].filename.replace("_"," ").title()
        for txt in text:
            em=discord.Embed(title=filename, description=f"```{txt}```", color=color())
            embeds.append(em)
        pag = self.bot.paginate(Paginator(embeds, per_page=1))
        await pag.start(ctx)

    @commands.command()
    @commands.has_guild_permissions(mention_everyone=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.guild_only()
    async def someone(self, ctx):
        await ctx.reply(random.choice([m for m in ctx.guild.members if not m.bot and m != ctx.author]).mention, mention_author=False)

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def shazam(self, ctx):
        attachment = None
        if ctx.message.reference:
            if ctx.message.reference.resolved.attachments:
                attachment = ctx.message.reference.resolved.attachments[0]
        elif ctx.message.attachments:
            attachment = ctx.message.attachments[0]

        if attachment is not None:
            if not attachment.url.endswith(".mp4"):
                em=discord.Embed(description="Please attach a video file", color=color())
                return await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description="Please attach a video file", color=color())
            return await ctx.reply(embed=em, mention_author=False)
        
        start_time = datetime.datetime.utcnow()
        em=discord.Embed(description=f"{self.bot.icons['loading']} Now downloading video...", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)
        path = tempfile.TemporaryDirectory()
        await attachment.save(f"{path.name}/file.mp4")
        em=discord.Embed(description=f"{self.bot.icons['loading']} Now recognizing song...", color=color())
        await msg.edit(embed=em)
        res = await client.recognize_song(path.name+"/file.mp4")
        try:
            track = res["track"]
        except KeyError:
            em=discord.Embed(description=f"{self.bot.icons['redtick']} Could not detect song", color=color())
            await msg.edit(embed=em, mention_author=False)
        else:
            title = track["title"]
            artist = track["subtitle"]
            await cleanup(path)
            em=discord.Embed(description=f"{self.bot.icons['loading']} Now fetching youtube information...", color=color())
            await msg.edit(embed=em)
            data = await youtube(f"{artist} {title}")
            try:
                url = "https://www.youtube.com/watch?v="+data["entries"][0]["id"]
            except Exception:
                url = "N/A"
            delta = datetime.datetime.utcnow() - start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            em=discord.Embed(color=color())
            em.add_field(name="Title", value=title, inline=False)
            em.add_field(name="Artist", value=artist, inline=False)
            em.add_field(name="URL", value=url, inline=False)
            em.set_footer(text=f"Finished in {minutes}m, {seconds}s")
            try:
                em.set_thumbnail(url=data["entries"][0]["thumbnail"])
            except Exception:
                pass
            await msg.edit(embed=em)

    @commands.group(invoke_without_command=True, aliases=["yt"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def youtube(self, ctx, *, query):
        async with ctx.typing():
            data = await youtube(query)
        
        try:
            data = data["entries"][0]
        except KeyError:
            data = data
        if data == [] and len(data) == 0:
            return await ctx.reply("I could not find a video with that query", mention_author=False)

        url = "https://www.youtube.com/watch?v="+data["id"]
        em=discord.Embed(title=data["title"], url=url, color=color())
        em.add_field(name="Channel", value=f"[{data['channel']}]({data['channel_url']})", inline=True)
        em.add_field(name="Duration", value=str(datetime.timedelta(seconds=data['duration'])), inline=True)
        em.add_field(name="Views", value=humanize.intcomma(data['view_count']))
        em.set_footer(text="Use the reactions for downloading")
        em.set_thumbnail(url=data["thumbnail"])
        msg = await ctx.reply(embed=em, mention_author=False)

        reactions = ["📼", "🔈"]

        for r in reactions:
            await msg.add_reaction(r)

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) in reactions and user == ctx.author and reaction.message == msg, timeout=30)
        except asyncio.TimeoutError:
            pass
        else:
            if str(reaction.emoji) == reactions[0]:
                for r in reactions:
                    await msg.remove_reaction(r, self.bot.user)
                await ctx.invoke(self.bot.get_command("youtube mp4"), **{"url": url})
            elif str(reaction.emoji) == reactions[1]:
                for r in reactions:
                    await msg.remove_reaction(r, self.bot.user)
                await ctx.invoke(self.bot.get_command("youtube mp3"), **{"url": url})

    @youtube.command(aliases=["video"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def mp4(self, ctx, url):
        if not re.search(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$", url):
            await ctx.reply("That is not a valid youtube video url", mention_author=False)
        else:
            start_time = datetime.datetime.utcnow()

            em=discord.Embed(description=f"{self.bot.icons['loading']} Now downloading video", color=color())
            msg = await ctx.reply(embed=em, mention_author=False)

            async with ctx.typing():
                res = await download(url)

            em=discord.Embed(description=f"{self.bot.icons['loading']} Now uploading video", color=color())
            await msg.edit(embed=em)

            delta = datetime.datetime.utcnow() - start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            try:
                await ctx.reply(content=f"Download took: {minutes}m, {seconds}s", file=res, mention_author=False)
            except discord.HTTPException:
                em=discord.Embed(description="The video was too large to be sent", color=color())
                await ctx.reply(embed=em, mention_author=False)

    @youtube.command(aliases=["audio"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def mp3(self, ctx, url):
        if not re.search(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$", url):
            em=discord.Embed(description="That is not a valid youtube video url", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            start_time = datetime.datetime.utcnow()
            async with ctx.typing():
                data = self.ytdl.extract_info(url, download=False)

            if data["duration"] > 900:
                raise TooLong("The video cannot be longer than 15 minutes.")
            else:
                try:
                    data = data["entries"][0]
                except IndexError:
                    em=discord.Embed(description="I could not find a video with that query", color=color())
                    return await ctx.reply(embed=em, mention_author=False)
                except KeyError:
                    data = data

                em=discord.Embed(description=f"{self.bot.icons['loading']} Now downloading audio", color=color())
                msg = await ctx.reply(embed=em, mention_author=False)

                async with ctx.typing():
                    res = await (await self.bot.session.get(data["url"])).read()

                em=discord.Embed(description=f"{self.bot.icons['loading']} Now uploading audio", color=color())
                await msg.edit(embed=em)
                
                delta = datetime.datetime.utcnow() - start_time
                hours, remainder = divmod(int(delta.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                try:
                    await ctx.reply(content=f"Download took: {minutes}m, {seconds}s", file=discord.File(io.BytesIO(res), filename=f"{data['title']}.mp3"), mention_author=False)
                except discord.HTTPException:
                    em=discord.Embed(description="The video was too large to be sent", color=color())
                    await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojiinfo(self, ctx, emoji: typing.Union[discord.PartialEmoji, discord.Emoji, str]):
        if isinstance(emoji, discord.PartialEmoji):
            em=discord.Embed(title=emoji.name, color=color())
            em.add_field(
                name="Created At",
                value=f"{emoji.created_at.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(emoji.created_at)})",
                inline=True
            )
            em.add_field(
                name="Animated?",
                value="".join(self.bot.icons['greentick'] if emoji.animated == True else self.bot.icons['redtick']),
                inline=True
            )
            em.set_thumbnail(url=str(emoji.url)+"?size=1024")
            em.set_footer(text=f"ID: {emoji.id}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(emoji, discord.Emoji):
            em=discord.Embed(title=emoji.name, color=color())
            em.add_field(
                name="Guild",
                value=f"""
{self.bot.icons['arrow']}Name: {emoji.guild.name}
> {emoji.guild.description}

{self.bot.icons['arrow']}Created At: {emoji.guild.created_at.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(emoji.guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(emoji.guild.verification_level).title()}
""", inline=True
            )
            em.add_field(
                name="Created At",
                value=f"{emoji.created_at.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(emoji.created_at)})",
                inline=True
            )
            em.add_field(
                name="Animated?",
                value="".join(self.bot.icons['greentick'] if emoji.animated == True else self.bot.icons['redtick']),
                inline=True
            )
            em.set_thumbnail(url=str(emoji.url)+"?size=1024")
            em.set_footer(text=f"ID: {emoji.id}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(emoji, str):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"This command does not support default emojis, please input a custom emoji", color=color())
            
            await ctx.reply(embed=em, mention_author=False)


    @commands.command(aliases=["shorten"])
    @commands.cooldown(1,10, commands.BucketType.user)
    async def shortener(self, ctx, url, custom_url = None):
        async with ctx.typing():
            if custom_url is None:
                res = list(isgd.shorten(url=url))[0]
            else:
                res = list(isgd.shorten(url=url, custom_url=custom_url))[0]
        em=discord.Embed(description=f"Here's your [shortened url]({res})", color=color())
        
        em.set_thumbnail(url="https://support.rebrandly.com/hc/article_attachments/360020801793/rebrandly_url_shortener_010.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, aliases=["emoji"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def emojis(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command})

    @emojis.command(aliases=["opt-in"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def optin(self, ctx):
        try:
            await self.bot.db.execute("INSERT INTO emojis (user_id) VALUES ($1)", ctx.author.id)
        except asyncpg.UniqueViolationError:
            em=discord.Embed(description=f"You've already opted into the emojis program", color=color())
            
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Alright! I've successfully opted you into the emojis program", color=color())
            
            await ctx.reply(embed=em, mention_author=False)

    @emojis.command(aliases=["opt-out"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def optout(self, ctx):
        res = await self.bot.db.fetchrow("SELECT user_id FROM emojis WHERE user_id = $1", ctx.author.id)
        try:
            res["user_id"]
        except TypeError:
            em=discord.Embed(description=f"You aren't opted into the emojis program", color=color())
            
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Alright! I've successfully opted you out of the emojis program", color=color())
            
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="sha256")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _sha(self, ctx, *, message):
        res = hashlib.sha256(message.encode()).hexdigest()
        await ctx.reply(res, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pypi(self, ctx, package):
        try:
            res = await self.bot.session.get(f"https://pypi.org/pypi/{package}/json")
            json = await res.json()
            name = json["info"]["name"] + " " + json["info"]["version"]
            author = json["info"]["author"] or "N/A"
            author_email = json["info"]["author_email"] or "N/A"
            url = json["info"]["project_url"] or "N/A"
            description = json["info"]["summary"] or "N/A"
            author = json["info"]["author"] or "N/A"
            license_ = json["info"]["license"] or "N/A"
            try:
                documentation = json["info"]["project_urls"]["Documentation"] or "N/A"
            except Exception:
                documentation = "N/A"
            try:
                website = json["info"]["project_urls"]["Homepage"] or "N/A"
            except Exception:
                website = "N/A"
            keywords = json["info"]["keywords"] or "N/A"
            em=discord.Embed(
                title=name,
                description=f"""
{description}
{self.bot.icons['arrow']}**Author**: {author}
{self.bot.icons['arrow']}**Author Email**: {author_email}

{self.bot.icons['arrow']}**Website**: {website}
{self.bot.icons['arrow']}**Documentation**: {documentation}
{self.bot.icons['arrow']}**Keywords**: {keywords}
{self.bot.icons['arrow']}**License**: {license_}""",
                url=url,
                color=color()
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/381963689470984203/814267252437942272/pypi.png")
            
            await ctx.reply(embed=em, mention_author=False)
        except aiohttp.ContentTypeError:
            em=discord.Embed(description=f"This package wasn't found", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["g"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, query):
        async with ctx.typing():
            if ctx.channel.is_nsfw():
                safe_search_setting=False
                safe_search="Disabled"
            else:
                safe_search_setting=True
                safe_search="Enabled"
            try:
                results = await google.search(str(query), safesearch=safe_search_setting)
            except async_cse.NoResults:
                em=discord.Embed(description=f"I couldn't find any results for `{query}`", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                embeds = []
                image = None
                for res in results:
                    if isImage(res.image_url):
                        image = res.image_url
                embeds = []
                res = WrapList(results, 3)
                for txt in res:
                    em=discord.Embed(title=f"Results for: `{query}`", color=color())
                    em.set_footer(text=f"Safe-Search: {safe_search}", icon_url=ctx.author.avatar_url)
                    em.add_field(name=f"\uFEFF", value="\n".join(f"**[{str(res.title)}]({str(res.url)})**\n{str(res.description)}\n" for res in txt), inline=False)
                    if image is not None:
                        em.set_thumbnail(url=image)
                    embeds.append(em)
                pag = self.bot.paginate(Paginator(embeds, per_page=1))
                await pag.start(ctx)

    @commands.command(aliases=["gimage"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def googleimage(self, ctx, *, query):
        if ctx.channel.is_nsfw():
            safe_search_setting=False
            safe_search="Disabled"
        else:
            safe_search_setting=True
            safe_search="Enabled"
        async with ctx.typing():
            results = await google.search(query, safesearch=safe_search_setting, image_search=True)
            images = []
            for res in results:
                if isImage(res.image_url):
                    images.append(res)
        if images != [] and len(images) != 0:
            embeds = []
            for res in images:
                em=discord.Embed(description=f"[{res.title}]({res.url})", color=color())
                em.set_footer(text=f"Safe-Search: {safe_search}", icon_url=ctx.author.avatar_url)
                em.set_image(url=res.image_url)
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            em=discord.Embed(description=f"I couldn't find any images with the query `{query}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["trans", "tr"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, output : str, *, text : str):
        async with ctx.typing():
            translation = await do_translate(output, text)
            em = discord.Embed(color=color())
            em.add_field(name=f"Input [{translation.src.upper()}]", value=f"```{text}```", inline=True)
            em.add_field(name=f"Output [{translation.dest.upper()}]", value=f"```{translation.text}```", inline=True)
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def commits(self, ctx):
        github = self.bot.github.replace("https://github.com/", "").split("/")
        username, repo = github
        res = await self.bot.session.get(f"https://api.github.com/repos/{username}/{repo}/commits")
        res = await res.json()
        em = discord.Embed(title=f"Commits", description="\n".join(f"[`{commit['sha'][:6]}`]({commit['html_url']}) {commit['commit']['message']}" for commit in res[:5]), url=self.bot.github+"/commits", color=color())
        em.set_thumbnail(url="https://image.flaticon.com/icons/png/512%2F25%2F25231.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["guildav", "servericon", "serverav", "sav", "srvav"])
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
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color())
            else:
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color())
            em.set_image(url=ctx.guild.icon_url)
            em.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["si", "guildinfo", "gi"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        if ctx.guild.description is None:
            description=""
        else:
            description = ctx.guild.description
        
        bots = online = dnd = idle = offline = 0
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
        
        try:
            booster_role = ctx.guild.premium_subscriber_role.mention 
        except AttributeError:
            booster_role = "N/A"
        created_at = ctx.guild.created_at.strftime("%d/%m/%Y at %H:%M:%S")
        em=discord.Embed(title=ctx.guild.name, description=f"{description}", color=color())
        em.set_image(url=ctx.guild.banner_url)
        em.set_thumbnail(url=ctx.guild.icon_url)
        em.add_field(name="Members", value=f"""
{self.bot.icons['arrow']}Online: `{online}`
{self.bot.icons['arrow']}DND: `{dnd}`
{self.bot.icons['arrow']}Idle: `{idle}`
{self.bot.icons['arrow']}Offline: `{offline}`
{self.bot.icons['arrow']}Bots: `{bots}`""", inline=True)
        em.add_field(name="Boosts", value=f"""
{self.bot.icons['arrow']}Amount: `{ctx.guild.premium_subscription_count}`
{self.bot.icons['arrow']}Role: {booster_role}""",inline=True)
        em.add_field(name="Channels", value=f"""
{self.bot.icons['arrow']}All `{len(ctx.guild.channels)}`
{self.bot.icons['arrow']}Text: `{len(ctx.guild.text_channels)}`
{self.bot.icons['arrow']}Voice: `{len(ctx.guild.voice_channels)}`""", inline=True)
        em.add_field(name="Other", value=f"""
{self.bot.icons['arrow']}Owner: {ctx.guild.owner.mention}
{self.bot.icons['arrow']}Roles: `{len(ctx.guild.roles)}`
{self.bot.icons['arrow']}Region: `{ctx.guild.region}`
{self.bot.icons['arrow']}Created at: `{created_at}` ({humanize.naturaltime(ctx.guild.created_at)})""", inline=True)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ui", "whois"], description="A command to get information about the given member", usage="[@member]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
            
        if "offline" != str(member.mobile_status):
            platform = "Mobile"
        elif "offline" != str(member.desktop_status):
            platform = "Desktop"
        elif "offline" != str(member.web_status):
            platform = "Web"
        else:
            platform = "N/A"

        created_at = member.created_at.strftime("%d/%m/%Y at %H:%M:%S")
        joined_at = member.joined_at.strftime("%d/%m/%Y at %H:%M:%S")

        pronoun = await get_pronoun(self.bot, member)

        if member.top_role.name == "@everyone":
            top_role="N/A"
        else:
            top_role=member.top_role.mention

        join_position = sum(member.joined_at > m.joined_at if m.joined_at is not None else "1" for m in ctx.guild.members)

        em=discord.Embed(title=str(member), color=color())
        em.add_field(name="Info", value=f"""
{self.bot.icons['arrow']}Name: {member.name}
{self.bot.icons['arrow']}Nickname: {member.nick}
{self.bot.icons['arrow']}Status: {''.join(member.raw_status.title() if member.raw_status != "dnd" else "DND")}
{self.bot.icons['arrow']}Platform: {platform}
{self.bot.icons['arrow']}Pronoun: {pronoun}
{self.bot.icons['arrow']}Created at: {created_at} ({humanize.naturaltime(member.created_at)})""", inline=True)
        em.add_field(name="Guild", value=f"""
{self.bot.icons['arrow']}Roles: {len(member.roles)}
{self.bot.icons['arrow']}Top Role: {top_role}
{self.bot.icons['arrow']}Join Position: {join_position}
{self.bot.icons['arrow']}Joined at: {joined_at} ({humanize.naturaltime(member.joined_at)})""", inline=True)
        em.set_footer(text=f"ID: {member.id}", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["pronouns"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def pronoun(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        pronoun = await get_pronoun(self.bot, member)

        em=discord.Embed(description=f"{member.mention}'s pronouns are `{pronoun}`", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def suggest(self, ctx):
        em=discord.Embed(description=f"Please now enter your suggestion below or type `cancel` to cancel", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)
        try:
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.channel == ctx.channel and msg.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            em=discord.Embed(description="You took too long to respond, now ignoring next messages", color=color())
            await msg.edit(embed=em)
        else:
            if suggestion.content.lower() != "cancel":
                webhook = Webhook.from_url(str(get_config("SUGGESTIONS")), adapter=AsyncWebhookAdapter(self.bot.session))
                em=discord.Embed(description=f"```{suggestion.clean_content}```", color=color())
                em.set_footer(text=f"Suggestion by {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                attachment = None
                if ctx.message.attachments:
                    attachment = ctx.message.attachments[0].url
                if attachment is not None:
                    em.set_image(url=attachment)
                await webhook.send(embed=em)
                await suggestion.add_reaction(self.bot.icons['greentick'])
                em=discord.Embed(description="Your suggestion has been sent to the admins\nNote: abuse may get you blacklisted", color=color())
                await msg.edit(embed=em)
            else:
                await msg.delete()

    @commands.command(aliases=["firstmsg", "fmessage", "fmsg"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def firstmessage(self, ctx, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        
        message = None
        async for m in channel.history(limit=1, oldest_first=True):
            message = m

        content = message.content

        em=discord.Embed(title="First Message", color=color(), url=message.jump_url, timestamp=message.created_at)
        em.set_author(name=message.author, icon_url=message.author.avatar_url)
        if len(content) > 25:
            content = content[:22-3]+"..."

        if content is not None and len(content) != 0:
            em.add_field(name="Content", value=content, inline=False)

        if message.reference:
            em.add_field(name="Reply", value=f"[{message.reference.resolved.content}]({message.reference.resolved.jump_url})", inline=False)

        if message.attachments:
            em.add_field(name="Attachments", value=", ".join(f"[{message.attachment.index(a)}]({a.url})" for a in message.attachments))

        if message.attachments:
            if isImage(message.attachments[0].url):
                em.set_thumbnail(url=message.attachments[0].url)

        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["gif"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def giphy(self, ctx, *, query : str):
        query = query.replace(" ", "%20")
        res = await self.bot.session.get(f"https://api.giphy.com/v1/gifs/search?api_key={get_config('GIPHY')}&q={query}&limit=50&offset=0&rating=g&lang=en")
        res = await res.json()
        if res["data"] != [] and len(res["data"]) != 0:
            res = random.choice(res["data"])
            image = res["images"]["original"]["url"]
            em=discord.Embed(title=res["title"], url=res["url"], color=color())
            em.set_image(url=image)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find any results with the query `{query}`", color=color())
            await ctx.reply(embed=em, mention_author=False)


    @commands.command(aliases=["urban"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def urbandictionary(self, ctx, *, term):
        async with ctx.typing():
            res = await self.bot.session.get("http://api.urbandictionary.com/v0/define", params={"term": term})
        res = await res.json()
        if res["list"] != [] and len(res["list"]) != 0:
            embeds = []
            for i in res["list"]:
                if len(embeds) > 9:
                    break
                res = i
                definition = res["definition"].replace("[", "").replace("]", "")
                permalink = res["permalink"]
                upvotes = res["thumbs_up"]
                author = res["author"]
                example = res["example"].replace("[", "").replace("]", "")
                word = res["word"]
                em=discord.Embed(title=word, description=f"""
{self.bot.icons['arrow']}**Definition**:
{definition}
{self.bot.icons['arrow']}**Example**:
{example}""", url=permalink, color=color())
                em.set_footer(text=f"👍 {upvotes} • 👤 {author}", icon_url=ctx.author.avatar_url)
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            em=discord.Embed(description=f"I could not find any results for `{term}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["src"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def source(self, ctx, *, command_name : str = None):
        if command_name == None:
            em=discord.Embed(description=f"My source code can be found [here]({self.bot.github})", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            command = self.bot.get_command(command_name)
            if not command:
                em=discord.Embed(description=f"Couldn't find command `{command_name}`", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                try:
                    source_lines, _ = inspect.getsourcelines(command.callback)
                except (TypeError, OSError):
                    em=discord.Embed(description=f"Couldn't retrieve source for `{command_name}`", color=color())
                    await ctx.reply(embed=em, mention_author=False)
                else:
                    source_lines = ''.join(source_lines).split('\n')
                    src = textwrap.dedent("\n".join(line for line in source_lines))
                    await ctx.author.send(file=await getFile(src, "py"))
                    await ctx.message.add_reaction(self.bot.icons['greentick'])

    @commands.group(invoke_without_command=True)
    async def news(self, ctx, branch = "main"):
        news = await self.bot.db.fetchrow("SELECT * FROM news WHERE branch = $1", branch) 
        content = news["content"]
        author = self.bot.get_user(int(news['author']))
        updated = datetime.datetime.fromtimestamp(int(news["updated"]))
        em=discord.Embed(title=f"News on branch {branch}", description=content, color=color())
        if author is not None:
            em.set_footer(text=f"Author: {author} • Updated: {updated.strftime('%d/%m/%Y at %H:%M:%S')}", icon_url=author.avatar_url)
        else:
            em.set_footer(text=f"Author: N/A • Updated: {updated.strftime('%d/%m/%Y at %H:%M:%S')}")
        em.set_thumbnail(url="https://images.emojiterra.com/google/android-11/128px/1f4f0.png")
        await ctx.reply(embed=em, mention_author=False)

    @news.command(hidden=True, aliases=["update"])
    async def set(self, ctx, branch, *, content):
        await self.bot.db.execute("UPDATE news SET content = $1, author = $2, updated = $3 WHERE branch = $4", content, ctx.author.id, time.time(), branch)
        await ctx.message.add_reaction(self.bot.icons['greentick'])

    @news.command(hidden=True, aliases=["remove"])
    async def delete(self, ctx, branch):
        await self.bot.db.execute("DELETE FROM news WHERE branch = $1", branch)
        await ctx.message.add_reaction(self.bot.icons['greentick'])

    @news.command(hidden=True, aliases=["make"])
    async def create(self, ctx, branch, *, content):
        await self.bot.db.execute("INSERT INTO news (branch, author, updated, content) VALUES ($1, $2, $3, $4)", branch, ctx.author.id, time.time(), content)
        await ctx.message.add_reaction(self.bot.icons['greentick'])

    @news.command(hidden=True)
    async def rename(self, ctx, branch, name):
        await self.bot.db.execute("UPDATE news SET branch = $1, author = $2, updated = $3 WHERE branch = $4", name, ctx.author.id, time.time(), branch)
        await ctx.message.add_reaction(self.bot.icons['greentick'])

    @commands.command(name="avatar", aliases=["icon", "av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _avatar(self, ctx, member : discord.Member = None):
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
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color())
            else:
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color())
            em.set_image(url=member.avatar_url)
            em.set_author(name=f"{member}", icon_url=member.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["lc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lettercount(self, ctx, *, text):
        em=discord.Embed(description=f"Your text is {len(text)} letters long", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["wc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wordcount(self, ctx, *, text):
        text_list = text.split(" ")
        em=discord.Embed(description=f"Your text is {len(text_list)} words long", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def invite(self, ctx):
        em=discord.Embed(description=f"Here's my [invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["up"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.uptime
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        em=discord.Embed(title="Uptime", description=f"{days}d, {hours}h, {minutes}m, {seconds}s", color=color())
        em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Eo_circle_green_arrow-up.svg/1200px-Eo_circle_green_arrow-up.svg.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["botinfo", "about", "bi"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        async with ctx.typing():
            process = psutil.Process()
            p = pathlib.Path('./')
            version = sys.version_info
            em = discord.Embed(color=color())
            # File Stats
            files = classes = funcs = comments = lines = letters = 0
            for f in p.rglob("*.py"):
                files += 1
                with f.open() as of:
                    letters = sum(len(f.open().read()) for f in p.rglob("*.py"))
                    for line in of.readlines():
                        line = line.strip()
                        if line.startswith("class"):
                            classes += 1
                        if line.startswith("def"):
                            funcs += 1
                        if line.startswith("async def"):
                            funcs += 1
                        if "#" in line:
                            comments += 1
                        lines += 1
            # Embed
            owner = self.bot.get_user(self.bot.ownersid)
            em.add_field(name="Bot", value=f"""
{self.bot.icons['arrow']}**Guilds**: `{len(self.bot.guilds)}`
{self.bot.icons['arrow']}**Users**: `{len(self.bot.users)}`
{self.bot.icons['arrow']}**Commands**: `{len([cmd for cmd in list(set(self.bot.walk_commands())) if not cmd.hidden])}`
{self.bot.icons['arrow']}**Commands executed**: `{self.bot.cmdsSinceRestart}`""", inline=True)
            em.add_field(name="File Statistics", value=f"""
{self.bot.icons['arrow']}**Letters**: `{letters}`
{self.bot.icons['arrow']}**Files**: `{files}`
{self.bot.icons['arrow']}**Lines**: `{lines}`
{self.bot.icons['arrow']}**Functions**: `{funcs}`""", inline=True)
            em.add_field(name="Links", value=f"""
{self.bot.icons['arrow']}[Developer](https://discord.com/users/{owner.id}) ({owner})
{self.bot.icons['arrow']}[Source]({self.bot.github})
{self.bot.icons['arrow']}[Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)""", inline=True)
            em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_footer(text=f"Python {version[0]}.{version[1]}.{version[2]} • discord.py {discord.__version__}")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def unspoiler(self, ctx, *, msg : str = None):
        if msg is None:
            if ctx.message.reference:
                text = ctx.message.reference.resolved.clean_content
        else:
            text = msg
        await ctx.reply(text.replace("|", ""), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
    
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def spoiler(self, ctx, *, msg : str = None):
        if msg is None:
            if ctx.message.reference:
                text = ctx.message.reference.resolved.clean_content
        else:
            text = msg
        await ctx.reply("".join(f"||{letter}||" for letter in text), mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def spotify(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        activity = None
        for i in ctx.author.activities:
            if isinstance(i, discord.activity.Spotify):
                activity = i
        if activity is not None:
            em=discord.Embed(title=activity.title, color=color(), url=f"https://open.spotify.com/track/{activity.track_id}")
            artists = ", ".join(artist for artist in activity.artists)
            duration = activity.duration
            days, seconds = duration.days, duration.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            em.add_field(name="Artists", value=artists, inline=False)
            em.add_field(name="Album", value=activity.album, inline=False)
            em.add_field(name="Duration", value=f"{minutes}m {seconds}s", inline=False)
            em.set_thumbnail(url=activity.album_cover_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"{member.mention} isn't listening to spotify", color=color())
            await ctx.reply(embed=em, mention_author=False)
    
    @commands.command(aliases=["rp", "activity", "richpresence", "status"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def presence(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s activities", color=color())
        for activity in member.activities:
            if isinstance(activity, discord.activity.Spotify):
                artists = ", ".join(artist for artist in activity.artists)
                duration = activity.duration
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                em.add_field(
                    name=f"Spotify",
                    value=f"""
{self.bot.icons['arrow']}Title: `{activity.title}`
{self.bot.icons['arrow']}URL: [Click here](https://open.spotify.com/track/{activity.track_id})
{self.bot.icons['arrow']}Artists: `{artists}`
{self.bot.icons['arrow']}Album: `{activity.album}`
{self.bot.icons['arrow']}Duration: `{minutes}`m `{seconds}`s
""",
                    inline=True
                )
                em.set_thumbnail(url=activity.album_cover_url)
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
{self.bot.icons['arrow']}Text: `{activity.name}`
{self.bot.icons['arrow']}Emoji Name: {emojiName}
{self.bot.icons['arrow']}Emoji: {emoji}
""",
                    inline=True
                )
            elif isinstance(activity, discord.activity.Game):
                em.add_field(
                    name="Game",
                    value=f"{self.bot.icons['arrow']}Name: `{activity.name}`",
                    inline=True
                )
            elif isinstance(activity, discord.activity.Streaming):
                em.add_field(
                    name="Stream",
                    value=f"""
{self.bot.icons['arrow']}Title: `{activity.name}`
{self.bot.icons['arrow']}Platform: `{activity.platform}`
{self.bot.icons['arrow']}URL: [{activity.url.split("/")[3]}]({activity.url})
""", inline=True
                )
            else:
                try:
                    type = str(activity.type).lower().split("activitytype.")[1].title()
                except Exception:
                    type = "N/A"
                em.add_field(
                    name="Unknown",
                    value=f"""
{self.bot.icons['arrow']}Name: `{activity.name}`
{self.bot.icons['arrow']}Details: `{activity.details}`
{self.bot.icons['arrow']}Emoji: `{activity.emoji}`
{self.bot.icons['arrow']}Type: `{type}`
""",
                    inline=True
                )
        
        await ctx.reply(embed=em, mention_author=False)

    @commands.group(name="qr", invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _qr(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command":ctx.command})

    @_qr.command(name="create", aliases=["make"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _create(self, ctx, *, text):
        text = text.replace(" " ,"%20")
        async with ctx.typing():
            res = await (await self.bot.session.get(f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=200x200")).read()
        em=discord.Embed(color=color())
        f = discord.File(io.BytesIO(res), filename="qr.png")
        em.set_footer(text=f"Powered by qrserver.com", icon_url=ctx.author.avatar_url)
        em.set_image(url=f"attachment://qr.png")
        await ctx.reply(embed=em, file=f, mention_author=False)

    @_qr.command(name="read", aliases=["show"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _read(self, ctx, url : str = None):
        attachment = await getImage(ctx, url)
        res = await self.bot.session.get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={attachment}")
        res = await res.json()
        res = res[0]["symbol"][0]
        if res["error"] is None:
            await ctx.reply(res["data"], mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        else:
            em=discord.Embed(description=res["error"], color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["run", "tio"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def execute(self, ctx, language, *, code : codeblock_converter):
        res = (code.content
            .replace("{author.name}", ''.join(ctx.author.name if ctx.author.name is not None else "None"))
            .replace("{author.id}", ''.join(str(ctx.guild.id) if str(ctx.guild.id) is not None else "None"))
            .replace("{author.nick}", ''.join(ctx.author.nick if ctx.author.nick is not None else "None"))
            .replace("{server.name}", ''.join(ctx.guild.name if ctx.guild.name is not None else "None"))
            .replace("{server.members}", ''.join(str(ctx.guild.member_count) if str(ctx.guild.member_count) is not None else "None"))
            .replace("{channel.name}", ''.join(ctx.channel.name if ctx.channel.name is not None else "None"))
            .replace("{channel.topic}", ''.join(ctx.channel.topic if ctx.channel.topic is not None else "None")))
        tio= await async_tio.Tio()
        async with ctx.typing():
            res = await tio.execute(res, language=language)
            await tio.close()
        if len(res.stdout) > 2000:
            f = await getFile(res.stdout, filename="output")
            await ctx.reply(file=f, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.reply(f"```\n{res.stdout}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(aliases=["fortnite", "fn", "fnstats"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fortnitestats(self, ctx, username, *, platform):
        platforms = {
            "pc": "kbm",
            "computer": "kbm",
            "switch": "gamepad",
            "nintendo switch": "gamepad",
            "xbox": "gamepad",
            "xbox one": "gamepad",
            "playstation": "gamepad",
            "playstation 4": "gamepad",
            "ps":"gamepad",
            "ps4": "gamepad",
            "phone": "touch",
            "android": "touch",
            "iphone": "touch"
        }
        try:
            platformm = platforms[platform.lower()]
        except KeyError:
            em=discord.Embed(description=f"I couldn't find the platform `{platform}`", color=color())
            
            await ctx.reply(embed=em, mention_author=False)
        else:
            async with ctx.typing():
                res = await self.bot.session.get(f"https://api.fortnitetracker.com/v1/profile/{platformm}/{username}", headers={"TRN-Api-Key":get_config("FORTNITE")})
                res = await res.json()
            try:
                error = str(res["accountId"])
            except KeyError:
                em=discord.Embed(description=res["error"], color=color())
                
                await ctx.reply(embed=em, mention_author=False)
            else:
                accid = res["accountId"]
                avatar = res["avatar"]
                name = res["epicUserHandle"]
                recentMatches = res["recentMatches"]
                em=discord.Embed(title=name, color=color())
                em.set_footer(text=f"ID: {accid} • Powered by fortnitetracker.com", icon_url=ctx.author.avatar_url)
                em.set_thumbnail(url=avatar)
                amount = len(recentMatches)
                if amount > 1:
                    amount = 1
                for x in range(amount):
                    match = recentMatches[x]
                    type_ = match["playlist"]
                    kills = match["kills"]
                    playTime = match["minutesPlayed"]
                    score = match["score"]
                    em.add_field(
                        name=f"Latest Match",
                        value=f"""
{self.bot.icons['arrow']}Game Type: `{type_.title()}`
{self.bot.icons['arrow']}Kills: `{kills}`
{self.bot.icons['arrow']}Play Time: `{playTime}` minutes
{self.bot.icons['arrow']}Score: `{score}`
""",
                        inline=True
                    )
                await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.has_guild_permissions(manage_emojis=True)
    @commands.cooldown(1,15,commands.BucketType.user)
    async def dumpemojis(self, ctx):
        emojis = []
        async  with ctx.typing():
            for e in ctx.guild.emojis:
                res = await (e.url_as()).read()
                e = (f"{e.name}.png" if not e.animated else f"{e.name}.gif", io.BytesIO(res))
                emojis.append(e)
            res = await download_emojis(emojis)
        await ctx.reply(file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def snipe(self, ctx):
        try:
            msg = self.bot.message_cache[ctx.guild.id][ctx.channel.id]
        except KeyError:
            em=discord.Embed(description=f"There's no message to snipe", color=color())
            return await ctx.reply(embed=em, mention_author=False)

        content = msg.content

        if content is None or len(content) == 0:
            content = "*Message did not contain any content*"

        res = WrapText(content, 2048)
        embeds = []
        for word in res:
            em = discord.Embed(description=word, color=color(), timestamp=msg.created_at)
            em.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            if msg.reference:
                em.add_field(name="Reply", value=f"[Click here]({msg.reference.resolved.jump_url})", inline=False)

            if msg.attachments:
                em.add_field(name="Attachment", value=f"[Click here]({str(msg.attachments[0].url)})", inline=False)  

            embeds.append(em)

        pag = self.bot.paginate(Paginator(embeds, per_page=1))
        await pag.start(ctx)

    @commands.command(aliases=["ss"])
    @commands.is_nsfw()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def screenshot(self, ctx, website):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://api.screenshotmachine.com?key={get_config('SCREENSHOT')}&url={website}&dimension=1280x720&user-agent=Mozilla/5.0 (Windows NT 10.0; rv:80.0) Gecko/20100101 Firefox/80.0")
            res = io.BytesIO(await res.read())
            em=discord.Embed(color=color())
            em.set_image(url="attachment://screenshot.jpg")
            em.set_footer(text=f"Powered by screenshotmachine.com", icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(embed=em, file=discord.File(res, "screenshot.jpg"), mention_author=False)
        await msg.add_reaction("🚮")
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) == "🚮" and reaction.message == msg and not user.bot)
        await msg.delete()
        em=discord.Embed(description=f"The screenshot has been deleted by {user.mention}", color=color())
        await ctx.reply(embed=em, mention_author=False)


    @commands.command()
    @commands.cooldown(1,5, commands.BucketType.user)
    async def disabled(self, ctx):
        res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
        try:
            res["commands"]
        except TypeError:
            em=discord.Embed(description=f"There are no disabled commands", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            commands = res["commands"]
            commands = commands.split(",")
            if len(commands) != 0 and commands != ['']:
                em=discord.Embed(title="Disabled commands", description=", ".join(cmd for cmd in commands if cmd != ""), color=color())

                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"There are no disabled commands", color=color())
                await ctx.reply(embed=em, mention_author=False)

    @commands.group(aliases=["rtfd"], invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rtfm(self, ctx, query):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location=https://discordpy.readthedocs.io/en/latest&show-labels=false&label-labels=false")
            res = await res.json()
            nodes = res["nodes"]
        if nodes != {}:
            em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color())
            em.set_footer(text=f"Powered by idevision.net", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"No results found for `{query}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @rtfm.command(name="python", aliases=["py"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _python(self, ctx, query):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location=https://docs.python.org/3&show-labels=false&label-labels=false")
            res = await res.json()
            nodes = res["nodes"]
        if nodes != {}:
            em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color())
            em.set_footer(text=f"Powered by idevision.net", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"No results found for `{query}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @rtfm.command(aliases=["cs"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def custom(self, ctx, suffix, query):
        url = f"https://{suffix}.readthedocs.io/en/latest/"
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location={url}&show-labels=false&label-labels=false")
        if res.status == 200:
            res = await res.json()
            nodes = res["nodes"]
            if nodes != {}:
                em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color())
                em.set_footer(text=f"Powered by idevision.net", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"No results found for `{query}`", color=color())
                await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Invalid result, maybe [the url]({url}) was invalid", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def weather(self, ctx, state):
        state = state.replace(" ", "%20")
        async with ctx.typing():
            location = await self.bot.session.get(f"https://www.metaweather.com/api/location/search/?query={state}")
            location = await location.json()
            try:
                woeid = location[0]["woeid"]
            except Exception:
                em=discord.Embed(description=f"I couldn't retrieve the weather for `{state}`", color=color())
                
                await ctx.reply(embed=em, mention_author=False)
            else:
                results = await google.search(location[0]["title"], safesearch=True)
                image = None
                for res in results:
                    if res.image_url.endswith("png") or res.image_url.endswith("jpg") or res.image_url.endswith("jpeg") or res.image_url.endswith("webp"):
                        image = res.image_url
                res = await self.bot.session.get(f"https://www.metaweather.com/api/location/{woeid}")
                res = await res.json()
                res = res["consolidated_weather"][0]
                em=discord.Embed(title=location[0]["title"], description=f"""
{self.bot.icons['arrow']}Type: `{res["weather_state_name"]}`
{self.bot.icons['arrow']}Wind Direction: `{res["wind_direction_compass"]}`
{self.bot.icons['arrow']}Temperature: `{round(int(res["the_temp"]), 1)}`
{self.bot.icons['arrow']}Minimum Temperature: `{round(int(res["min_temp"]), 1)}`
{self.bot.icons['arrow']}Maximum Temperature: `{round(int(res["max_temp"]), 1)}`
{self.bot.icons['arrow']}Wind Speed: `{round(int(res["wind_speed"]), 1)}`
{self.bot.icons['arrow']}Air Pressure: `{round(int(res["air_pressure"]), 1)}`
{self.bot.icons['arrow']}Humidity: `{res["humidity"]}`
{self.bot.icons['arrow']}Visibility: `{round(int(res["visibility"]), 1)}`
""", color=color())
                if image is not None:
                    em.set_thumbnail(url=image)
                em.set_footer(text=f"Powered by metaweather.com", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def steam(self, ctx, steamid):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://api.snaz.in/v2/steam/user-profile/{steamid}")
        if res.status != 200:
            em=discord.Embed(description=f"I couldn't find the member `{steamid}`", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            res = await res.json()
            username = res["username"]
            if res["animated_background_url"] is None:
                if res["background_url"] is not None:
                    background = res["background_url"]
                else:
                    background = None
            else:
                background = res["animated_background_url"]
            avatar = res["avatar"]
            level = res["level"]["value"]
            location = "".join("N/A" if res["location"] == None else res["location"])
            real_name = "".join("N/A" if res["real_name"] == "" else res["real_name"])
            if res["primary_group"] is not None:
                group = res["primary_group"]["name"]
                group_url = res["primary_group"]["url"]
            else:
                group = None
            em=discord.Embed(title=username, url=f"https://steamcommunity.com/id/{steamid}", color=color())
            em.add_field(name="Level", value=level, inline=True)
            em.add_field(name="Real Name", value=real_name, inline=True)
            em.add_field(name="Location", value=location, inline=True)
            em.add_field(name="Primary Group", value="".join(f"[{group}]({group_url})" if group is not None else "N/A"), inline=True)
            em.add_field(name="Background URL", value="".join(f"[Click here]({background})" if background is not None else "N/A"), inline=True)
            if avatar is not None:
                em.set_thumbnail(url=avatar)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["corona", "coronavirus", "covid19"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def covid(self, ctx, *, country):
        country = country.replace(" ", "%20")
        async with ctx.typing():
            res = await self.bot.session.get("https://dinosaur.ml/covid19/countries_all/")
            res = (await res.read()).decode()
            res = json.loads(res)
            stats = None
            for c in res:
                if c["country"].lower() == country.lower():
                    stats = c
        if stats is not None:
            em=discord.Embed(title=f"Covid in {stats['country']}", description=f"""
{self.bot.icons['arrow']}Cases: {stats['cases']}
{self.bot.icons['arrow']}Deaths: {stats['deaths']}
{self.bot.icons['arrow']}Recovered: {stats['recovered']}
{self.bot.icons['arrow']}Active: {stats['active']}
{self.bot.icons['arrow']}Critical: {stats['critical']}
{self.bot.icons['arrow']}Cases Today: {stats['todayCases']}
{self.bot.icons['arrow']}Deaths Today: {stats['todayDeaths']}
{self.bot.icons['arrow']}Recovered Today: {stats['todayRecovered']}
""", color=color())
            em.set_footer(text="Powered by dinosaur.ml", icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=stats["countryInfo"]["flag"])
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find any covid stats for `{country}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["shard", "shards"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def shardinfo(self, ctx, shard : int = None):
        if shard is None:
            em=discord.Embed(title="Shards", color=color())
            for shard in list(self.bot.shards):
                shard = dict(self.bot.shards)[shard]
                em.add_field(
                    name=f"Shard {shard.id+1}",
                    value=f"""
{self.bot.icons['arrow']}Latency: `{round(shard.latency, 1)}`ms
{self.bot.icons['arrow']}Count: `{shard.shard_count}`
""", inline=True
                )
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["calculator", "calculater", "calc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def calculate(self, ctx, *, args : str):
        em=discord.Embed(color=color())
        try:
            res = mathjspy.MathJS().eval(args)
        except Exception as exc:
            em.add_field(name="Input", value=args, inline=True)
            em.add_field(name="Error", value=f"`{str(exc)}`", inline=True)
        else:
            em.add_field(name="Input", value=args, inline=True)
            em.add_field(name="Output", value=res, inline=True)
        em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Calculator_Flat_Icon_Vector.svg/512px-Calculator_Flat_Icon_Vector.svg.png")
        await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, command : str = None):
        prefix = (await get_prefix(self.bot, ctx.message))[2]
        if command is None:
            if ctx.author.id == self.bot.ownersid:
                prefix_msg = ''.join(f"The prefix for `{ctx.guild.name}` is `{prefix}` \n" if not self.bot.emptyPrefix else "")
            else:
                prefix_msg = f"The prefix for `{ctx.guild.name}` is `{prefix}` \n"
            em=discord.Embed(
                title="Help Page",
                description=f'''
{prefix_msg}```diff
- Type "{prefix}help [command]" or "{prefix}help [cog]"
- for more information about a command or cog
+ [] = optional argument
+ <> = required argument
```
[Developer](https://discord.com/users/{self.bot.ownersid}) | [Support]({self.bot.invite}) | [Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)
''',
                color=color()
            )
            
            if ctx.guild is not None:
                disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                try:
                    disabled = disabled["commands"]
                except Exception:
                    disabled = []
                else:
                    disabled = disabled.split(",")
            else:
                disabled = []
            cogs = []
            for cog in self.bot.cogs:
                cog = get_cog(self.bot, cog)
                if not cog.qualified_name.lower() in ["jishaku"]:
                    if is_mod(self.bot, ctx.author):
                        cmds = [cmd for cmd in cog.get_commands()]
                    else:
                        cmds = [cmd for cmd in list(cog.get_commands()) if not cmd.hidden]
                    if len(cmds) != 0 and cmds != []:
                        cogs.append(cog)
            em.add_field(
                name=f"Cogs [{len(cogs)}]",
                value="\n".join(f"`{cog.qualified_name}`" for cog in cogs),
                inline=True
            )
            news = await self.bot.db.fetchrow("SELECT * FROM news WHERE branch = 'main'")
            content = news["content"]
            updated = datetime.datetime.fromtimestamp(int(news["updated"]))
            em.add_field(
                name=f"News - {updated.strftime('%d %b %Y')}",
                value=content,
                inline=True
            )
            await ctx.reply(embed=em, mention_author=False)

        elif self.bot.get_command(str(command)) is not None:
            given_command = self.bot.get_command(str(command))
            disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
            try:
                disabled = disabled["commands"]
            except Exception:
                disabled = []
            else:
                disabled = disabled.split(",")
            if not given_command.hidden == True and not given_command.name in disabled or is_mod(self.bot, ctx.author):
                #-------------------------------------
                try:
                    command_subcommands = "> " + ", ".join(f"`{command.name}`" for command in given_command.commands if not command.hidden or not command.name in disabled)
                except Exception:
                    command_subcommands = "N/A"
                #-------------------------------------
                if given_command.usage is not None:
                    command_usage = given_command.usage
                else:
                    parameters = {}
                    for param in list(given_command.params):
                        if not param in ["self", "ctx"]:
                            parameter = dict(given_command.params)[str(param)]
                            if parameter.kind.name.lower() == "positional_or_keyword":
                                parameters[str(param)] = "required"
                            else:
                                parameters[str(param)] = "optional"
                    command_usage = " ".join(f"<{param}>" if dict(parameters)[param] == "required" else f"[{param}]" for param in list(parameters))
                #---------------------------------------
                command_bucket = given_command._buckets
                command_cooldown = command_bucket._cooldown
                if command_cooldown is not None:
                    cooldown_type = list(command_cooldown.type)[0]
                    cooldown_per = round(command_cooldown.per)
                    if cooldown_per > 59:
                        cooldown_per = f"{round(cooldown_per / 60)} minutes"
                    else:
                        cooldown_per = f"{cooldown_per} seconds"
                    cooldown_rate = command_cooldown.rate
                    cooldown_msg = f"{''.join(f'{cooldown_rate} time' if str(cooldown_rate) == '1' else f'{cooldown_rate} times')} every {cooldown_per} per {cooldown_type}"
                else:
                    cooldown_msg = "N/A"
                #---------------------------------------
                command_name = None
                if given_command.parent is not None:
                    command_name = f"{given_command.parent.name} {given_command.name}"
                else:
                    command_name = given_command.name
                #---------------------------------------
                em=discord.Embed(
                    title=command_name,
                    description=given_command.description,
                    color=color()
                )
                
                em.add_field(name="Usage", value=f"{prefix}{command_name} {command_usage}", inline=False)
                em.add_field(name="Cooldown", value=cooldown_msg, inline=False)
                if given_command.aliases:
                    em.add_field(name=f"Aliases [{len(given_command.aliases)}]", value="> " + ", ".join(f"`{alias}`" for alias in given_command.aliases), inline=False)
                else:
                    em.add_field(name="Aliases [0]", value="N/A", inline=False)
                try:
                    if is_mod(self.bot, ctx.author):
                        commands_ = [cmd for cmd in given_command.commands]
                    else:
                        commands_ = [cmd for cmd in given_command.commands if not cmd.hidden and not cmd.name in disabled]
                except Exception:
                    commands_ = "N/A"
                try:
                    em.add_field(name=f"Subcommands [{''.join(str(len(commands_)) if str(commands_) != 'N/A' else '0')}]", value=command_subcommands, inline=False)
                except AttributeError:
                    em.add_field(name=f"Subcommands [0]", value="N/A", inline=False)
                em.add_field(name="Category", value=given_command.cog_name, inline=False)
                await ctx.reply(embed=em, mention_author=False)
        else:
            disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
            try:
                disabled = disabled["commands"]
            except Exception:
                disabled = []
            else:
                disabled = disabled.split(",")
            given_cog = get_cog(self.bot, command)
            if given_cog is not None:
                if is_mod(self.bot, ctx.author):
                    commands_ = [cmd for cmd in given_cog.walk_commands() if cmd.parent is None]
                else:
                    commands_ = [cmd for cmd in given_cog.walk_commands() if not cmd.hidden and not cmd.name in disabled and cmd.parent is None]
                if commands_ is not None and commands_ != []:
                    em=discord.Embed(title=f"{given_cog.qualified_name} commands [{len(commands_)}]", description=f"{given_cog.description}\n\n> "+", ".join(f"`{cmd.name}`" for cmd in commands_), color=color())
                    await ctx.reply(embed=em, mention_author=False)
                else:
                    await ctx.reply(f"This command does not exist", mention_author=False)
            else:
                await ctx.reply(f"There isn't a cog / command with the name `{command}`", mention_author=False)

    @help.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def all(self, ctx):
        em=discord.Embed(
            title="All Commands",
            timestamp=datetime.datetime.utcnow(),
            color=color()
        )
        for cog in self.bot.cogs:
            cog = get_cog(self.bot, cog)
            if is_mod(self.bot, ctx.author):
                cmds = [cmd for cmd in list(cog.get_commands())]
            else:
                cmds = [cmd for cmd in list(cog.get_commands()) if not cmd.hidden]
            if len(cmds) != 0 and cmds != []:
                em.add_field(
                    name=f"{cog.qualified_name} ({len(cog.get_commands())})",
                    value="> " + ", ".join(command.name for command in cmds),
                    inline=False
                )
        await ctx.author.send(embed=em)
        await ctx.message.add_reaction("📬")

    @commands.command(name="file", aliases=["makefile", "createfile"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _file_(self, ctx, *, content : str = None):
        if content is None:
            if not ctx.message.reference:
                raise commands.MissingRequiredArgument(inspect.Parameter("content", inspect.Parameter.KEYWORD_ONLY))
            elif ctx.message.reference.resolved.content is None or len(ctx.message.reference.resolved.content) == 0:
                raise commands.MissingRequiredArgument(inspect.Parameter("content", inspect.Parameter.KEYWORD_ONLY))
            else:
                content = ctx.message.reference.resolved.content
        f = await getFile(content)
        await ctx.reply(file=f, mention_author=False)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def minecraft(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=name, description=f"""
{self.bot.icons['arrow']}Name: `{name}`
{self.bot.icons['arrow']}UID: `{uid}`
""", color=color(), url=f"https://namemc.com/profile/{name}")
            em.set_thumbnail(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size=256")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def avatar(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s avatar", color=color(), url=f"https://namemc.com/profile/{name}")
            em.set_image(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size128")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def skin(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s skin", color=color(), url=f"https://namemc.com/profile/{name}")
            em.set_image(url=f"https://crafatar.com/renders/body/{uid}?default=MHF_Steve&overlay&scale=5")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def head(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s head", color=color(), url=f"https://namemc.com/profile/{name}")
            em.set_image(url=f"https://crafatar.com/renders/head/{uid}?default=MHF_Steve&overlay&scale=5")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def friends(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            res = await self.bot.session.get(f"https://api.namemc.com/profile/{uid}/friends")
            res = await res.json()
            if res != []:
                em=discord.Embed(title=f"{name}'s friends", color=color(), url=f"https://namemc.com/profile/{name}")
                for friend in list(res):
                    em.add_field(
                        name=friend["name"],
                        value=f"""
{self.bot.icons['arrow']}Name: `{friend['name']}`
{self.bot.icons['arrow']}UUID: `{friend['uuid']}`
{self.bot.icons['arrow']}[NameMC](https://namemc.com/profile/{friend['name']})
""",
                        inline=True
                    )
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"`{name}` has no friends on namemc.com", color=color(), url=f"https://namemc.com/profile/{name}")
                em.set_thumbnail(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size=256")
                await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def inviteinfo(self, ctx, invite):
        try:
            invite = await self.bot.fetch_invite(invite)
        except discord.NotFound:
            em=discord.Embed(description=f"I couldn't find this invite", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            guild = invite.guild
            if guild.description is not None:
                em=discord.Embed(title=guild.name,description=f"""
    > {guild.description}

{self.bot.icons['arrow']}Created at: {guild.created_at.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(guild.verification_level).title()}""", color=color(), url=invite)
            else:
                em=discord.Embed(title=guild.name,description=f"""
{self.bot.icons['arrow']}Created at: {guild.created_at.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(guild.verification_level).title()}""", color=color(), url=invite)
            em.set_thumbnail(url=guild.icon_url)
            em.set_footer(text=f"ID: {guild.id}", icon_url=ctx.author.avatar_url)
            if guild.banner_url is not None:
                em.set_image(url=guild.banner_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        em=discord.Embed(title="🏓 Pong", description=f"{self.bot.icons['loading']} Now measuring latency...", color=color())
        start=time.perf_counter()
        msg = await ctx.reply(embed=em, mention_author=False)
        end=time.perf_counter()
        final=end-start
        typing = round(final*1000)

        poststart = time.perf_counter()
        await self.bot.db.fetch("SELECT 1")
        postduration = (time.perf_counter()-poststart) * 1000
        db_ping = round(postduration, 1)

        em=discord.Embed(title="🏓 Pong", color=color())
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.add_field(name="Websocket", value=f"{round(self.bot.latency*1000)}ms", inline=True)
        em.add_field(name="Typing", value=f"{typing}ms", inline=True)
        em.add_field(name="Database", value=f"{db_ping}ms", inline=True)
        await msg.edit(embed=em)

    @commands.command()
    async def afk(self, ctx, *, reason : str = None):
        if reason is None:
            msg = f"Okay, I've marked you as afk"
        else:
            msg = f"Okay, I've marked you as afk for `{reason}`"
        em=discord.Embed(description=msg, color=color())
        await ctx.reply(embed=em, mention_author=False)
        await asyncio.sleep(3)
        self.bot.afks[ctx.author.id] = {"reason": reason}

    @commands.command(aliases=["rawmsg"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rawmessage(self, ctx, message : discord.Message = None):
        if ctx.message.reference:
            msg = await self.bot.http.get_message(int(ctx.message.reference.channel_id), int(ctx.message.reference.message_id))
        elif message:
            msg = await self.bot.http.get_message(int(message.channel.id), int(message.id))
        else:
            msg = await self.bot.http.get_message(int(ctx.channel.id), int(ctx.message.id))
        raw = json.dumps(msg, indent=4)
        em=discord.Embed(
            description=f"```json\n{discord.utils.escape_markdown(raw)}```",
            timestamp=datetime.datetime.utcnow(),
            color=color()
        )
        if len(em.description) < 2048:
            await ctx.reply(embed=em, mention_author=False)
        else:
            f = await getFile(raw, "json")
            await ctx.reply(file=f, mention_author=False)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def ocr(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, url)

        res = await self.bot.session.get(url)

        image = await res.read()

        if url.lower().endswith("png"):
            filetype = "png"
        elif url.lower().endswith("jpg"):
            filetype = "jpg"
        elif url.lower().endswith("jpeg"):
            filetype = "jpeg"
        elif url.lower().endswith("webp"):
            filetype = "webp"
        else:
            filetype = None
        
        async with ctx.typing():
            res = (await (await self.bot.session.get("https://idevision.net/api/public/ocr", headers={"Authorization":get_config("IDEVISION")}, params={"filetype":filetype}, data=image)).json())["data"]

        text = WrapText(res, 2048)
        if len(text) == 0:
            return await ctx.reply("I couldn't read what your image says", mention_author=False)
        embeds = []
        for txt in text:
            em=discord.Embed(description=txt, color=color())
            em.set_footer(text=f"Powered by idevision.net", icon_url=ctx.author.avatar_url)
            embeds.append(em)
        pag = self.bot.paginate(Paginator(embeds, per_page=1))
        await pag.start(ctx)

def setup(bot):
    bot.add_cog(Utility(bot))
