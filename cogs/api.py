import discord, datetime, io
from jishaku.codeblocks import codeblock_converter
from discord.ext import commands
from utils.get import *

class API(commands.Cog):

    """API commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def cat(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://api.thecatapi.com/v1/images/search")
        res = await res.json()
        image = res[0]["url"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by thecatapi.com", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def window(self, ctx, *, text : codeblock_converter):
        url = self.bot.config["SECRET_API"]
        data = {
            "paddingVertical": "56px",
            "paddingHorizontal": "56px",
            "backgroundImage": None,
            "backgroundImageSelection": None,
            "backgroundMode": "color",
            "backgroundColor": "rgba(26,127,220,0.62)",
            "dropShadow": True,
            "dropShadowOffsetY": "20px",
            "dropShadowBlurRadius": "68px",
            "theme": "vscode",
            "windowTheme": "none",
            "language": "".join(text.language if text.language is not None else "auto"),
            "fontFamily": "Hack",
            "fontSize": "14px",
            "lineHeight": "133%",
            "windowControls": True,
            "widthAdjustment": True,
            "lineNumbers": False,
            "firstLineNumber": 1,
            "exportSize": "2x",
            "watermark": False,
            "squaredImage": False,
            "hiddenCharacters": False,
            "name": "",
            "width": 680,
            "code": text.content,
        }
        async with ctx.typing():
            img = io.BytesIO(await (await self.bot.session.post(url, json=data)).read())
        em=discord.Embed(color=self.bot.color)
        em.set_image(url=f"attachment://window.png")
        await ctx.reply(embed=em, file=discord.File(img, filename=f"window.png"), mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def xkcd(self, ctx, number : int = None):
        async with ctx.typing():
            latest = await (await self.bot.session.get("https://xkcd.com/info.0.json")).json()
        res = None
        if number is None:
            res = latest
        elif latest["num"] < number:
            return await ctx.reply(f"This number is not available, the current maximum is {latest['num']}", mention_author=False)
        
        if res is None:
            async with ctx.typing():
                res = await (await self.bot.session.get(f"https://xkcd.com/{number}/info.0.json")).json()

        em=discord.Embed(title=res["title"], description=res["alt"], color=self.bot.color)
        em.set_image(url=res["img"])
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def dog(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://dog.ceo/api/breeds/image/random")
        res = await res.json()
        image = res["message"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by dog.ceo", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bunny(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://api.bunnies.io/v2/loop/random/?media=gif")
        res = await res.json()
        image = res["media"]["gif"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by bunnies.io", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def duck(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://random-d.uk/api/v1/random?type=png")
        res = await res.json()
        image = res["url"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by random-d.uk", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fox(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://randomfox.ca/floof/")
        res = await res.json()
        image = res["image"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by randomfox.ca", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lizard(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://nekos.life/api/v2/img/lizard")
        res = await res.json()
        image = res["url"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by nekos.life", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def shiba(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("http://shibe.online/api/shibes")
        res = await res.json()
        image = res[0]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by shibe.online", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def koala(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/img/koala")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def panda(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/img/panda")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bird(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/img/bird")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def pikachu(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/img/pikachu")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True)
    async def fact(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command})
    
    @fact.command(name="dog")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _dog(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/dog")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @fact.command(name="cat")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _cat(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/cat")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)
    
    @fact.command(name="panda")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _panda(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/panda")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def chucknorris(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://api.chucknorris.io/jokes/random")
        res = await res.json()
        fact = res["value"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by chucknorris.io", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)
    
    @fact.command(name="fox")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _fox(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/fox")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)
    
    @fact.command(name="bird")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _bird(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/bird")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)
    
    @fact.command(name="koala")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _koala(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://some-random-api.ml/facts/koala")
        res = await res.json()
        fact = res["fact"]
        em=discord.Embed(description=fact, color=self.bot.color, timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by some-random-api.ml", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)
    

def setup(bot):
    bot.add_cog(API(bot))