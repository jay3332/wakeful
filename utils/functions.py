import os, tempfile, discord, io, typing, re
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

def isImage(url):
    if url.endswith("png") or url.endswith("jpg") or url.endswith("jpeg") or url.endswith("webp"):
        return True
    return False

def getImage(ctx : commands.Context, url : typing.Union[discord.Member, discord.Emoji, discord.PartialEmoji, None, str] = None):
    if ctx.message.reference:
        ref = ctx.message.reference.resolved
        if ref.embeds:
            if ref.embeds[0].image.url != discord.Embed.Empty:
                if isImage(ref.embeds[0].image.url):
                    return ref.embeds[0].image.url
                    
        elif ref.attachments:
            url = ref.attachments[0].url or ref.attachments[0].proxy_url
            if isImage(url):
                return url

    if url is None:
        return str(ctx.author.avatar_url_as(format="png", size=1024))

    if isinstance(url, discord.Member):
        return str(url.avatar_url_as(format="png", size=1024))
    elif isinstance(url, str):
        if re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url) and isImage(url):
            return url

    if isinstance(url, discord.Emoji) or isinstance(url, discord.PartialEmoji):
        return url.url

    if ctx.message.attachments:

        if isImage(ctx.message.attachments[0].url) or isImage(ctx.message.attachments[0].proxy_url):
            return ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url

        elif isinstance(url, discord.Member):
            return str(url.avatar_url_as(format="png", size=1024))
        else:
            return str(ctx.author.avatar_url_as(format="png", size=1024))

    else:
        return str(ctx.author.avatar_url_as(format="png", size=1024))