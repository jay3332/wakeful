import discord, typing, io
import twemoji_parser as twemoji

from pilmoji import Pilmoji
from PIL import Image, ImageFont
from discord.ext import commands
from utils.get import *
from __main__ import get_prefix


class Miscellaneous(commands.Cog):
    
    """Commands that aren't really useful or fun, so commands that are just there"""

    def __init__(self, bot):
        self.bot = bot

    @executor_function
    def emojitoimg(self, emoji):
        with Image.new('RGBA', (400, 400), 0) as image:
            font = ImageFont.truetype('data/font.ttf', 24)
            with Pilmoji(image) as pilmoji:
                pilmoji.text((0,0), str(emoji), (0, 0, 0), font, emoji_position_offset=(0, 5), emoji_size_factor=16.7)
        buffer = io.BytesIO()
        image.save(buffer, "png")
        buffer.seek(0)
        return buffer

    @commands.command(aliases=["be"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bigemoji(self, ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji, str]):
        if isinstance(emoji, str):
            emoji = await twemoji.emoji_to_url(emoji)
        else:
            emoji = emoji.url

        try:
            emoji.animated
        except AttributeError:
            emoji_animated = False
        else:
            emoji_animated = emoji.animated
        
        async with ctx.typing():
            res = await (await self.bot.session.get(str(emoji))).read()
        await ctx.reply(file=discord.File(io.BytesIO(res), filename="emoji."+"".join("png" if not emoji_animated else "gif")), mention_author=False)
    
    @commands.command(aliases=["eti"], description="Similar to bigemoji, difference is, that it renders it. Note: it doesn't support animated emojis")
    @commands.cooldown(1,15,commands.BucketType.user)
    async def emojitoimage(self, ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji, str]):
        async with ctx.typing():
            res = await self.emojitoimg(emoji)
        await ctx.reply(file=discord.File(res, filename="".join(f"{emoji}.png" if isinstance(emoji, str) else f"{emoji.name}.png")), mention_author=False)

    @commands.command(description=f'''
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

        em=discord.Embed(description=f"{question}\n\n{answers}", color=color())
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(embed=em, mention_author=False)

        for e in questions:
            res = questions[e]["emoji"]
            await msg.add_reaction(res)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
