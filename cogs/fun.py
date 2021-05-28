import discord, io, asyncdagpi, asyncio, datetime, aiohttp, string, random, json
from discord.ext import commands
from gtts import gTTS
from jishaku.functools import executor_function
from utils.get import get_config
from utils.configs import color

dagpi = asyncdagpi.Client(get_config("DAGPI"))

@executor_function
def do_tts(language, message):
    epix = io.BytesIO()
    tts = gTTS(text=message, lang=language)
    tts.write_to_fp(epix)
    epix.seek(0)
    file = discord.File(epix, f"{message}.wav")
    return file

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text = ""):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.trigger_typing()
        try:
            attachment = ctx.message.attachments[0]
        except:
            attachment = None
        if not attachment:
            await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.send(text, file=await attachment.to_file(), allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *, message):
        async with ctx.typing():
            file = await do_tts("en", message)
        await ctx.reply(file=file, mention_author=False)

    @commands.command(aliases=["gtl"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guessthelogo(self, ctx):
        async with ctx.typing():
            logo = await dagpi.logo()
            answer = logo.answer
            brand = logo.brand
            hint = logo.hint
            question = logo.question
            embed = discord.Embed(description=f"try guessing this logo in under 20 seconds - hint: ||`{hint}`||", color=color(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=question)
            embed.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        emsg = await ctx.send(embed=embed)
        try:
            brand = logo.brand
            msg = await self.bot.wait_for('message', check=lambda message: message.content.lower() == str(brand).lower() and message.channel == ctx.channel and message.author == ctx.author, timeout=20)
            em=discord.Embed(description=f"correct! the logo was `{brand}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=logo.answer)
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
            await emsg.edit(embed=em)
        except asyncio.TimeoutError:
            em=discord.Embed(description=f"you took too long to answer, it was `{logo.brand}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=logo.answer)
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
            await emsg.edit(embed=em)
        
    @commands.command(description="Gets the http cat image of the given number", usage="[http code]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def httpcat(self, ctx, code : int):
        res = await self.bot.session.get("https://http.cat/{code}")
        buf = io.BytesIO(await res.read())
        file=discord.File(buf, filename=f"{code}.png")
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=f"attachment://{code}.png")
        em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):
        async with ctx.typing():
            joke = await dagpi.joke()
            em = discord.Embed(description=joke, color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(name="8ball")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        async with ctx.typing():
            response = await dagpi.eight_ball()
            em = discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.add_field(name="input", value=f"```\n{question}```", inline=False)
            em.add_field(name="output", value=f"```\n{response}```", inline=False)
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roast(self, ctx):
        async with ctx.typing():
            roast = await dagpi.roast()
            em = discord.Embed(description=roast, color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(usage="[file]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def caption(self, ctx, member : discord.Member = None):
        if not member:
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]
                url = attachment.proxy_url
            else:
                em=discord.Embed(description=f"missing required argument `member / attachment`", color=color())
                await ctx.send(embed=em)
                return
        else:
            url = str(member.avatar_url_as(static_format="png", size=1024))
        async with ctx.typing():
            data = {
                "Content": url,
                "Type": "CaptionRequest",
            }
            headers = {"Content-Type": "application/json; charset=utf-8"}
            async with self.bot.session as cs:
                async with cs.post("https://captionbot.azurewebsites.net/api/messages", data=json.dumps(data), headers=headers) as res:
                    text = await res.text()
            em=discord.Embed(description=text, color=color())
            em.set_image(url=member.avatar_url_as(format="png"))
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        letters=[]
        for letter in text:
            if letter in string.ascii_letters:
                letters.append(letter)
            else:
                if letter == " ":
                    letters.append(" ")
        if letters != []:
            try:
                em=discord.Embed(timestamp=datetime.datetime.utcnow(), color=color())
                em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                em.add_field(name="input", value=f"```{text}```", inline=False)
                em.add_field(name="output", value="".join(f":regional_indicator_{letter}:" if not letter == " " else " " for letter in letters), inline=False)
                await ctx.send(embed=em)
            except discord.HTTPException:
                em=discord.Embed(description="the output was too long to be sent", color=color())
                em.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)
        else:
            em=discord.Embed(description="​", color=color())
            em.set_footer(text=f"is this what you want? • requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(fun(bot))