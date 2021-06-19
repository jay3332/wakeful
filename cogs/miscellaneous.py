import discord, typing, io
from discord.ext import commands
from utils.get import *
from __main__ import get_prefix


class Miscellaneous(commands.Cog):
    
    """Commands that aren't really useful or fun, so commands that are just there"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bigemoji(self, ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji]):
        async with ctx.typing():
            res = await (await self.bot.session.get(str(emoji.url))).read()
        await ctx.reply(file=discord.File(io.BytesIO(res), filename="emoji."+"".join("png" if not emoji.animated else "gif")), mention_author=False)

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
