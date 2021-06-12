import json, discord, typing, functools, asyncio
import youtube_dl as ydl

def executor_function(sync_function: typing.Callable):
    """A decorator that wraps a sync function in an executor, changing it into an async function.

    This allows processing functions to be wrapped and used immediately as an async function.

    Examples
    ---------

    Pushing processing with the Python Imaging Library into an executor:

    .. code-block:: python3

        from io import BytesIO
        from PIL import Image

        from jishaku.functools import executor_function


        @executor_function
        def color_processing(color: discord.Color):
            with Image.new('RGB', (64, 64), color.to_rgb()) as im:
                buff = BytesIO()
                im.save(buff, 'png')

            buff.seek(0)
            return buff

        @bot.command()
        async def color(ctx: commands.Context, color: discord.Color=None):
            color = color or ctx.author.color
            buff = await color_processing(color=color)

            await ctx.send(file=discord.File(fp=buff, filename='color.png'))
    """

    @functools.wraps(sync_function)
    async def sync_wrapper(*args, **kwargs):
        """
        Asynchronous function that wraps a sync function with an executor.
        """

        loop = asyncio.get_event_loop()
        internal_function = functools.partial(sync_function, *args, **kwargs)
        return await loop.run_in_executor(None, internal_function)

    return sync_wrapper

@executor_function
def youtube(query, download = False):
    ytdl = ydl.YoutubeDL({"format": "bestaudio/best", "restrictfilenames": True, "noplaylist": True, "nocheckcertificate": True, "ignoreerrors": True, "logtostderr": False, "quiet": True, "no_warnings": True, "default_search": "auto", "source_address": "0.0.0.0"})
    info =  ytdl.extract_info(query, download=download)
    del ytdl
    return info

def get_config(string : str):
    with open("config.json", "r") as f:
        conf = json.load(f)
    return conf[string]

def get_cog(bot, name):
    for cog in bot.cogs:
        cog = bot.get_cog(cog)
        if cog.qualified_name.lower() == name.lower():
            return cog
    
def color():
    return int(get_config("COLOR"), 16)

async def get_pronoun(bot : typing.Union[discord.Client, discord.ext.commands.Bot], member : discord.Member):
    pronouns={
        "hh": "he/him",
        "hi": "he/it",
        "hs": "/he/she",
        "ht": "he/they",
        "ih": "it/him",
        "ii": "it/its",
        "is": "it/she",
        "it": "it/they",
        "shh": "she/he",
        "sh": "she/her",
        "si": "she/it",
        "st": "she/they",
        "th": "they/he",
        "ti": "they/it",
        "ts": "they/she",
        "tt": "they/them",
        "any": "Any",
        "other": "Other",
        "ask": f"Ask",
        "avoid": "No pronoun, use name",
        "None": "N/A"
    }
    res = await (await bot.session.get(f"https://pronoundb.org/api/v1/lookup?id={member.id}&platform=discord")).json()
    try:
        code = res["pronouns"]
    except KeyError:
        code = "None"
    return pronouns[code]