import os, tempfile, discord, collections
from discord.ext import commands
from jishaku.functools import executor_function

@executor_function
def makeFile(text, end, filename):
    file_ = tempfile.NamedTemporaryFile()
    file_.write(text.encode())
    file_.seek(os.SEEK_SET)
    yield discord.File(file_.name, filename=f"{filename}.{end}")
    file_.close()

async def getFile(text, end = "txt", filename="message"):
    result = await makeFile(text, end, filename)
    return list(set(result))[0]

async def makeEmbed(context : commands.Context, embed : discord.Embed, mention : bool = False):
    embed = embed.to_dict()
    file_ = None
    if len(embed["description"]) > 1024:
        file_ = getFile(embed["description"])
    if file_ is not None:
        await context.reply(embed=discord.Embed().from_dict(embed), mention_author=mention, file=file_)
    else:
        embed["description"] == "The description was too large, so I've put it into a file"
        await context.reply(embed=discord.Embed().from_dict(embed), mention_author=mention)
