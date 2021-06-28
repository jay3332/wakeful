import discord, asyncio
import async_cleverbot as ac
from discord.ext import commands
from utils.get import *


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.member)
    async def chatbot(self, ctx):
        em=discord.Embed(description="Alright! I've started the chatbot, you can now talk to him, to cancel use `chat stop`, `chat close` or `chat cancel`", color=self.bot.color)
        await ctx.reply(embed=em, mention_author=False)
        cleverbot = ac.Cleverbot(self.bot.config["CLEVERBOT"])
        while True:
            try:
                msg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=30)
            except asyncio.TimeoutError:
                em=discord.Embed(description="I've stopped the chatbot, as you've not been responding for 30 seconds", color=self.bot.color)
                await msg.reply(embed=em, mention_author=False)
                break
            else:
                if msg.content.lower() in ["chat stop", "chat close", "chat cancel"]:
                    em=discord.Embed(description="Alright! I've successfully stopped the chatbot", color=self.bot.color)
                    await msg.reply(embed=em, mention_author=False)
                    break
                else:
                    async with ctx.typing():
                        res = await cleverbot.ask(msg.content, msg.author.id)
                        await msg.reply(res.text, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        return

def setup(bot):
    bot.add_cog(Chatbot(bot))
