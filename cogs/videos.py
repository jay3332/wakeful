import discord, io, aiohttp
from discord.ext import commands


class Videos(commands.Cog):

    """Commands for editing videos, remember, it can take a while for the processed video to be sent"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["vc"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def videocaption(self, ctx, *, text: str):
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"cap={text}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def muffle(self, ctx, amount: int):

        if amount > 100 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 100")
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"muffle={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def reverb(self, ctx, amount: int):

        if amount > 100 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 100")
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"reverb={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def disco(self, ctx, amount: int):

        if amount > 100 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 100")
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"disco={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command(aliases=["vv"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def videovolume(self, ctx, amount: int):
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"volume={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def shake(self, ctx, amount: int):

        if amount > 100 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 100")
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"shake={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sketch(self, ctx, amount: int):

        if amount > 100 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 100")
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"sketch={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command(aliases=["bndc"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def bandicam(self, ctx):
 
        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"bndc")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command(aliases=["df"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def deepfry(self, ctx, amount: int):

        if amount > 10 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 10")

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"df={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def speed(self, ctx, *, amount: float):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"speed={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @speed.command(aliases=["v"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def video(self, ctx, *, amount: float):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"vspeed={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @speed.command(aliases=["a"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def audio(self, ctx, *, amount: float):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"aspeed={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def reverse(self, ctx):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"reverse")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @reverse.command(name="video", aliases=["v"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def _video(self, ctx):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"vreverse")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @reverse.command(name="audio", aliases=["a"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def _audio(self, ctx):

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"areverse")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def spin(self, ctx, amount: int):

        if amount > 10 or amount < 1:
            return await ctx.send("Please provide an amount that is over 1 and under 10")

        attachment = None

        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith(".mp4"):
                attachment = ctx.message.attachments[0]

        if attachment is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved.attachments:
                    ref = ctx.message.reference.resolved
                    if ref.attachments[0].url.endswith(".mp4"):
                        attachment = ref.attachments[0]
        
        if attachment is None:
            return await ctx.send("Please attach an mp4 file")

        async with ctx.processing(ctx):
            file = await attachment.read()
            f = aiohttp.FormData()
            f.add_field("file",
                        io.BytesIO(file),
                        filename="video.mp4",
                        content_type="video/mp4")
            f.add_field("commands", f"spin={str(amount)}")
            res = await self.bot.session.post("https://pigeonburger.xyz/api/v1/edit/", headers={"EVB_AUTH": self.bot.config["EVB"]}, data=f)

        data = await res.json()

        if data["error"] == True:
            return await ctx.send(f"{data['code']} {data['message']}")

        await ctx.send(file=discord.File(io.BytesIO(await (await self.bot.session.get((data)["media_url"])).read()), filename="video.mp4"))

def setup(bot):
    bot.add_cog(Videos(bot))
