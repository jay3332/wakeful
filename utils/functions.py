import os, tempfile, discord, io
from discord.ext import commands
from jishaku.functools import executor_function

@executor_function
def getFile(text, end = "txt", filename="message"):
    f = io.StringIO()
    f.write(text)
    f.seek(0)
    return discord.File(f, filename=f"{filename}.{end}")

async def makeEmbed(context : commands.Context, embed : discord.Embed, mention : bool = False):
    embed = embed.to_dict()
    file_ = None
    if len(embed["description"]) > 1024:
        file_ = await getFile(embed["description"])
    if file_ is not None:
        await context.reply(embed=discord.Embed().from_dict(embed), mention_author=mention, file=file_)
    else:
        embed["description"] == "The description was too large, so I've put it into a file"
        await context.reply(embed=discord.Embed().from_dict(embed), mention_author=mention)