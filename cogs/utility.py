import discord, datetime, async_cse, psutil, humanize
from discord.ext import commands
from utils.configs import color
from moviepy.editor import *
from jishaku.functools import executor_function

google = async_cse.Search(os.getenv("GOOGLE"))

class utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["g"], description="a command to find results of the given term on google", usage="[term]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, term):
        async with ctx.typing():
            if ctx.channel.is_nsfw():
                safe_search_setting=False
                safe_search="disabled"
            else:
                safe_search_setting=True
                safe_search="enabled"
            value=0
            results = await google.search(str(term), safesearch=safe_search_setting)
            em=discord.Embed(
                title=f"results for: `{term}`",
                timestamp=datetime.datetime.utcnow(),
                color=color()
            ).set_footer(text=f"requested by {ctx.author.name}#{ctx.author.discriminator} | safe-search: {safe_search}", icon_url=ctx.author.avatar_url)
            for result in results:
                if not value > 4:
                    epic = results[int(value)]
                    em.add_field(
                        name=f" \uFEFF",
                        value=f"**[{str(epic.title)}]({str(epic.url)})**\n{str(epic.description)}\n",
                        inline=False
                    )
                    value+=1
        await ctx.send(embed=em)

    @commands.command(aliases=["lc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lettercount(self, ctx, *, text):
        em=discord.Embed(description=f"your text is {len(text)} letters long", color=color())
        await ctx.send(embed=em)

    @commands.command(aliases=["wc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wordcount(self, ctx, *, text):
        text_list = text.split(" ")
        em=discord.Embed(description=f"your text is {len(text_list)} words long", color=color())
        await ctx.send(embed=em)

    @commands.command(aliases=["botinfo", "about"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        operating_system=None
        if os.name == "nt":
            operating_system = "windows"
        elif os.name == "posix":
            operating_system = "linux"
        await ctx.trigger_typing()
        process = psutil.Process()
        version = sys.version_info
        embed = discord.Embed(color=color())
        delta_uptime = datetime.datetime.utcnow() - self.bot.uptime
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed.add_field(name="bot", value=f"- **guilds**: `{len(self.bot.guilds)}`\n- **users**: `{len(self.bot.users)}`\n- **commands**: `{len(self.bot.commands)}`\n- **cogs**: `{len(self.bot.cogs)}`\n- **uptime**: `{days}d {hours}h {minutes}m {seconds}s`", inline=True)
        embed.add_field(name="system", value=f"- **os**: `{operating_system}`\n- **cpu**: `{process.cpu_percent()}`%\n- **memory**: `{humanize.naturalsize(process.memory_full_info().rss).lower()}`\n- **process**: `{process.pid}`\n- **threads**: `{process.num_threads()}`", inline=True)
        embed.add_field(name="code", value=f"- **language**: `python`\n- **python version**: `{version[0]}.{version[1]}.{version[2]}`\n- **discord.py version**: `{discord.__version__}`", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=embed)

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=color())
            await destination.send(embed=emby)

def setup(bot):
    bot.help_command = MyNewHelp()
    bot.add_cog(utility(bot))