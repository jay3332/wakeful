import discord
import typing
import io
import inspect
import twemoji_parser as twemoji
from wand import image
from discord.ext import commands
from utils.get import *


class Miscellaneous(commands.Cog):
    
    """Commands that aren't really useful or fun, so commands that are just there"""

    def __init__(self, bot):
        self.bot = bot

    @executor_function
    def svg2png(self, bytes_):
        with image.Image(blob=bytes_, format="svg", width=400, height=400, background="none") as svg:
            data = svg.make_blob("png")
        return io.BytesIO(data)

    @commands.command(aliases=["svg2png"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def svgtopng(self, ctx, attachment: str = None):
        if attachment is None:
            if not ctx.message.attachments:
                raise commands.MissingRequiredArgument(inspect.Parameter("attachment", inspect.Parameter.KEYWORD_ONLY))
        
        if attachment is None:
            url = ctx.message.attachments[0].url or ctx.message.attachments[0].proxy_url
        else:
            url = attachment

        if not url.endswith(".svg"):
            return await ctx.reply("Please give me a valid svg file")

        res = await (await self.bot.session.get(url)).read()

        image = await self.svg2png(res)

        await ctx.reply(file=discord.File(image, filename=ctx.command.name+".png"), mention_author=False)

    @commands.command(aliases=["be"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bigemoji(self, ctx, emoji: typing.Union[discord.Emoji, discord.PartialEmoji, str]):

        try:
            emoji_animated = emoji.animated
        except AttributeError:
            try:
                emoji_animated = emoji.is_animated
            except AttributeError:
                emoji_animated = False

        if isinstance(emoji, str):
            emoji = await twemoji.emoji_to_url(emoji)
        else:
            emoji = emoji.url
        
        async with ctx.processing(ctx):
            res = await (await self.bot.session.get(str(emoji))).read()

        await ctx.reply(file=discord.File(io.BytesIO(res), filename="".join("emoji.gif" if emoji_animated else "emoji.png")), mention_author=False)

    @commands.command(description='''
Example: `poll "Am I cool?" Yes=✅,No=❌`
''')
    @commands.cooldown(1,5,commands.BucketType.user)
    async def poll(self, ctx, question, *, options):
        options = options.split(",")
        questions = {}
        for a in options:
            res = a.split("=")
            questions[a] = {"question": res[0], "emoji": res[1]}

        answers = "\n".join(f"{questions[e]['question']} - {questions[e]['emoji']}" for e in options)

        em=discord.Embed(description=f"{question}\n\n{answers}", color=self.bot.color)
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(embed=em, mention_author=False)

        for e in questions:
            res = questions[e]["emoji"]
            await msg.add_reaction(res)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
