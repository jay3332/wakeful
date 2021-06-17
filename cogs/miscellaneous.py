import discord, typing, io
from discord.ext import commands
from utils.get import *


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Commands that aren't really useful or fun, so commands that are just there"""

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bigemoji(self, ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji]):
        async with ctx.typing():
            res = await (await self.bot.session.get(str(emoji.url))).read()
        await ctx.reply(file=discord.File(io.BytesIO(res), filename="emoji.png"), mention_author=False)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
