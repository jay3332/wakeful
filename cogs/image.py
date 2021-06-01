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
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pixel(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def america(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.america(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triggered(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triggered(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wasted(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wasted(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def invert(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.invert(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sobel(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.sobel(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triangle(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triangle(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def blur(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.blur(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def angel(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.angel(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["s8n"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def satan(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.satan(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def delete(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.delete(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def fedora(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.fedora(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["hitler"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def worsethanhitler(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.hitler(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wanted(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wanted(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def jail(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.jail(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pride(self, ctx, flag : str = "gay", member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pride(), url=url, flag=flag)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def trash(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.trash(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def magik(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.magik(), url=url)
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def paint(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
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
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.captcha(), url=url, text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)


def setup(bot):
    bot.add_cog(image(bot))