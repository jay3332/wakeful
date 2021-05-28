import discord, json, asyncio, importlib
from discord.ext import commands
from utils.configs import color
from utils.checks import is_mod

status_types = {
    "dnd": discord.Status.dnd,
    "online": discord.Status.online,
    "invis": discord.Status.offline,
    "invisible": discord.Status.offline,
    "offline": discord.Status.offline,
    "sleep": discord.Status.idle,
    "sleeping": discord.Status.idle,
    "idle": discord.Status.idle
}

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blacklist(self, ctx):
        return

    @blacklist.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def add(self, ctx, user : discord.User):
        if is_mod(self.bot, user):
            with open("blacklist.json", "r") as f:
                blacklist = json.load(f)
            blacklist[str(user.id)] = ""
            with open("blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=4)
            em=discord.Embed(description=f"successfully blacklisted {user}", color=color())
            await ctx.send(embed=em)

    @blacklist.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def remove(self, ctx, user : discord.User):
        if is_mod(self.bot, user):
            with open("blacklist.json", "r") as f:
                blacklist = json.load(f)
            blacklist.pop(str(user.id), None)
            with open("blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=4)
            em=discord.Embed(description=f"successfully unblacklisted {user}", color=color())
            await ctx.send(embed=em)

    @commands.group(invoke_without_command=True, aliases=["rp", "richpresence", "activity"])
    async def status(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), {"command": ctx.command.name})

    @status.command()
    async def streaming(self, ctx, url, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Streaming(name=str(game), url=f'https://www.twitch.tv/{url.lower()}'))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def playing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(name=game))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def watching(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=3))
            await ctx.message.add_reaction("✅")

    @status.command()
    async def listening(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=2))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def competing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=5))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command(aliases=["default", "original"])
    async def reset(self, ctx):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(self.bot.guilds)} guilds & {len(self.bot.users)} users"))
            self.bot.status = None
            await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        proc = await asyncio.create_subprocess_shell("git pull", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout:
            shell = stdout.decode()
        if stderr:
            shell = stderr.decode()
        em=discord.Embed(description=f"```sh\n{shell}```", color=color())
        await ctx.send(embed=em)
        await self.bot.close() # close the bot, so systemd will start it right back up

def setup(bot):
    bot.add_cog(admin(bot))