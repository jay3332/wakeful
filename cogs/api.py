import discord, io, asyncio, datetime, aiohttp,json
from discord.ext import commands
from utils.configs import color

class api(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def cat(self, ctx):
        res = await self.bot.session.get("https://api.thecatapi.com/v1/images/search")
        res = await res.json()
        image = res[0]["url"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by thecatapi.com • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def dog(self, ctx):
        res = await self.bot.session.get("https://dog.ceo/api/breeds/image/random")
        res = await res.json()
        image = res["message"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by dog.ceo • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bunny(self, ctx):
        res = await self.bot.session.get("https://api.bunnies.io/v2/loop/random/?media=gif")
        res = await res.json()
        image = res["media"]["gif"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by bunnies.io • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def duck(self, ctx):
        res = await self.bot.session.get("https://random-d.uk/api/v1/random?type=png")
        res = await res.json()
        image = res["url"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by random-d.uk • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fox(self, ctx):
        res = await self.bot.session.get("https://randomfox.ca/floof/")
        res = await res.json()
        image = res["image"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by randomfox.ca • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lizard(self, ctx):
        res = await self.bot.session.get("https://nekos.life/api/v2/img/lizard")
        res = await res.json()
        image = res["url"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by nekos.life • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def shiba(self, ctx):
        res = await self.bot.session.get("http://shibe.online/api/shibes")
        res = await res.json()
        image = res[0]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by shibe.online • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def koala(self, ctx):
        res = await self.bot.session.get("https://some-random-api.ml/img/koala")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by some-random-api.ml • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def panda(self, ctx):
        res = await self.bot.session.get("https://some-random-api.ml/img/panda")
        res = await res.json()
        image = res["link"]
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=image)
        em.set_footer(text=f"powered by some-random-api.ml • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(api(bot))