import discord, io, asyncdagpi, asyncio, datetime, aiohttp, string, random, json, wonderwords, time
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

@executor_function
def typeracer(img, sentence):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("data/font.ttf", 150)
    draw.text((0, 0),str(sentence),(0,0,0),font=font)
    array = io.BytesIO()
    img.save(array, format="png")
    return discord.File(io.BytesIO(array.getvalue()), "typeracer.png")

class Fun(commands.Cog):

    """Fun & games commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *, message):
        async with ctx.typing():
            file = await do_tts("en", message)
        await ctx.reply(file=file, mention_author=False)

    @commands.command(aliases=["typerace"], description="Makes the bot send an image with text, which someone has to type in 20 seconds")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def typeracer(self, ctx):
        async with ctx.typing():
            start_time = datetime.datetime.utcnow()
            sentence = wonderwords.RandomSentence().sentence()
            img = await self.bot.session.get("https://media.discordapp.net/attachments/832746281335783426/850000934658244668/typeracer.jpg")
            _file = await typeracer(io.BytesIO(await img.read()), sentence)
            em=discord.Embed(description="First one to type this sentence wins", color=color())
            em.set_image(url="attachment://typeracer.png")
            _msg = await ctx.reply(embed=em, file=_file, mention_author=False)
        try:
            msg = await self.bot.wait_for("message", check=lambda message: message.content == str(sentence) and message.channel == ctx.channel, timeout=60)
            delta = datetime.datetime.utcnow() - start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            em=discord.Embed(description=f"We have a winner! {msg.author.mention} has typed the sentence in `{seconds}` seconds", color=color())
            await _msg.edit(embed=em)
        except asyncio.TimeoutError:
            em=discord.Embed(description=f"No one sent the right sentence, it was `{sentence}`", color=color())
            await _msg.edit(embed=em)

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
            embed.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        emsg = await ctx.send(embed=embed)
        try:
            brand = logo.brand
            msg = await self.bot.wait_for('message', check=lambda message: message.content.lower() == str(brand).lower() and message.channel == ctx.channel and message.author == ctx.author, timeout=20)
            em=discord.Embed(description=f"correct! the logo was `{brand}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=logo.answer)
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
            await emsg.edit(embed=em)
        except asyncio.TimeoutError:
            em=discord.Embed(description=f"you took too long to answer, it was `{logo.brand}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=logo.answer)
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
            await emsg.edit(embed=em)
        
    @commands.command(description="Gets the http cat image of the given number", usage="[http code]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def httpcat(self, ctx, code : int):
        res = await self.bot.session.get(f"https://http.cat/{code}")
        buf = io.BytesIO(await res.read())
        file=discord.File(buf, filename=f"{code}.png")
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=f"attachment://{code}.png")
        em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):
        async with ctx.typing():
            joke = await dagpi.joke()
            em = discord.Embed(description=joke, color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="8ball")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        async with ctx.typing():
            response = await dagpi.eight_ball()
            em = discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.add_field(name="input", value=f"```\n{question}```", inline=False)
            em.add_field(name="output", value=f"```\n{response}```", inline=False)
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roast(self, ctx):
        async with ctx.typing():
            roast = await dagpi.roast()
            em = discord.Embed(description=roast, color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ppsize"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def pp(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s pp", description="8"+"".join("=" for x in range(random.randrange(0,10)))+"D", color=color())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def gayrate(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s gayrate", description=f"{member.name} is `{random.randrange(0,100)}`% gay", color=color())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(usage="[file]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def caption(self, ctx, member : discord.Member = None):
        if not member:
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]
                url = attachment.proxy_url
            else:
                url = str(ctx.author.avatar_url_as(static_format="png", size=1024))
        else:
            url = str(member.avatar_url_as(static_format="png", size=1024))
        async with ctx.typing():
            data = {
                "Content": url,
                "Type": "CaptionRequest"
            }
            headers = {"Content-Type": "application/json; charset=utf-8"}
            res = await self.bot.session.post("https://captionbot.azurewebsites.net/api/messages", json=data, headers=headers)
            text = await res.text()
            em=discord.Embed(description=text, color=color())
            em.set_image(url=url)
        await ctx.reply(embed=em, mention_author=False)

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
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                em.add_field(name="Input", value=f"```{text}```", inline=False)
                em.add_field(name="Output", value="".join(f":regional_indicator_{letter}:" if not letter == " " else " " for letter in letters), inline=False)
                await ctx.reply(embed=em, mention_author=False)
            except discord.HTTPException:
                em=discord.Embed(description="The output was too long to be sent", color=color())
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description="​", color=color())
            em.set_footer(text=f"Is this what you want? • Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(Fun(bot))
