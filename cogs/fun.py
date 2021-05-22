import discord, io
from discord.ext import commands
from gtts import gTTS
from jishaku.functools import executor_function

@executor_function
def do_tts(language, message):
    epix = io.BytesIO()
    tts = gTTS(text=message, lang=language)
    tts.write_to_fp(epix)
    epix.seek(0)
    file = discord.File(epix, f"{message}.wav")
    return file

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text = ""):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.trigger_typing()
        try:
            attachment = ctx.message.attachments[0]
        except:
            attachment = None
        if not attachment:
            await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.send(text, file=await attachment.to_file(), allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *, message):
        async with ctx.typing():
            file = await do_tts("en", message)
        await ctx.reply(file=file, mention_author=False)

def setup(bot):
    bot.add_cog(fun(bot))