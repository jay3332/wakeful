import discord, polaroid, io

from discord.ext import commands

from jishaku.functools import executor_function
from utils.functions import *
from utils.get import *

@executor_function
def do_polaroid(image, method : str, args : list = [], kwargs : dict = {}):
    img = polaroid.Image(image)
    method = getattr(img, method)
    method(*args, **kwargs)
    bytes_ = img.save_bytes()
    file = discord.File(io.BytesIO(bytes_), filename=f"{method}.png")
    return file

class Polaroid(commands.Cog):

    """Commands for image manipulation, using python's [polaroid](https://pypi.org/project/polaroid/) module"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rainbow(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="apply_gradient")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def mirror(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="fliph")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def flip(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="flipv")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def blur(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="box_blur")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wide(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="resize", args=(2000,900,1))
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def brighten(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await self.bot.session.get(image)
            img = await img.read()
        res = await do_polaroid(img, method="brighten", kwargs={"treshold":50})
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def solarize(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="solarize")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def oil(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="oil", kwargs={"radius":5, "intensity":5})
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def filter(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command":ctx.command.name})

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def cali(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def dramatic(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def firenze(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def golden(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lix(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lofi(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def neue(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def obsidian(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def pink(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=["pastel_pink"])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ryo(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def oceanic(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def marine(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def seagreen(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)
    
    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def flagblue(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def liquid(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def diamante(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def radio(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def twenties(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rosetint(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def mauve(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bluechrome(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def vintage(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)

    @filter.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def serenity(self, ctx, url : typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            image = str(getImage(ctx, url))
            img = await (await self.bot.session.get(image)).read()
            res = await do_polaroid(img, method="filter", args=[ctx.command.name])
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(embed=em, file=res, mention_author=False)


def setup(bot):
    bot.add_cog(Polaroid(bot))
