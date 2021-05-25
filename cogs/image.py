import discord, asyncdagpi, datetime
from discord.ext import commands
from utils.get import get_config
from utils.configs import color

dagpi = asyncdagpi.Client(get_config("DAGPI"))

class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pixel(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pixel(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def america(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.america(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triggered(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triggered(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wasted(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wasted(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def invert(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.invert(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sobel(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.sobel(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triangle(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triangle(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def blur(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.blur(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def angel(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.angel(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["s8n"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def satan(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.satan(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def delete(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.delete(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def fedora(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.fedora(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["hitler"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def worsethanhitler(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.hitler(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wanted(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wanted(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def jail(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.jail(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pride(self, ctx, flag : str = "gay", member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pride(), url=str(member.avatar_url_as(static_format="png", size=1024)), flag=flag)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def trash(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.trash(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def magik(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.magik(), url=str(member.avatar_url_as(static_format="png", size=1024)))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def paint(self, ctx, member : discord.Member = None):
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
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.paint(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def captcha(self, ctx, text : str, member : discord.Member = None):
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
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.captcha(), url=url, text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)


def setup(bot):
    bot.add_cog(image(bot))