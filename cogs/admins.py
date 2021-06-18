import discord, asyncio, os, pwd, random
from discord.ext import commands
from utils.checks import is_mod
from utils.functions import *
from utils.get import *
from utils.paginator import *
from jishaku.models import copy
from jishaku.codeblocks import codeblock_converter
from prettytable import PrettyTable

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

class Admin(commands.Cog):

    """Commands for administrators"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["dev"], hidden=True)
    async def developer(self, ctx):
        if is_mod(self.bot, ctx.author):
            await ctx.invoke(self.bot.get_command("help"), **{"command":"developer"})

    @developer.command(aliases=["del"])
    @commands.is_owner()
    async def delete(self, ctx):
        if not ctx.message.reference:
            em=discord.Embed(description="Please reply to the message you want to delete", color=color)
            return await ctx.reply(embed=em, mention_author=False)
        ref = ctx.message.reference.resolved
        if ref.author != self.bot.user:
            em=discord.Embed(description="This command is only to delete my messages", color=color())
            return await ctx.reply(embed=em, mention_author=False)
        await ref.delete()
        try:
            await ctx.message.delete()
        except Exception:
            pass


    @commands.group(invoke_without_command=True, hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blacklist(self, ctx):
        pass

    @blacklist.command(hidden=True)
    async def add(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            await self.bot.db.fetch("INSERT INTO blacklist (user_id) VALUES ($1)", user.id)
            em=discord.Embed(description=f"Successfully blacklisted {user.mention}", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @blacklist.command(hidden=True)
    async def remove(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            await self.bot.db.fetch("DELETE FROM blacklist WHERE user_id = $1", user.id)
            em=discord.Embed(description=f"Successfully unblacklisted {user.mention}", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @blacklist.command(hidden=True)
    async def check(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            try:
                thing = await self.bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", user.id)
                thing["user_id"]
            except TypeError:
                em=discord.Embed(description=f"{user.mention} isn't blacklisted", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"{user.mention} is blacklisted", color=color())
                await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, name="setstatus", aliases=["setrp", "setrichpresence", "setactivity"], hidden=True)
    async def status(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command.name})

    @status.command(hidden=True)
    async def streaming(self, ctx, url, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Streaming(name=str(game), url=f'https://www.twitch.tv/{url.lower()}'))
            await ctx.message.add_reaction(self.bot.icons['greentick'])
            self.bot.status = ""

    @status.command(hidden=True)
    async def playing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(name=game))
            await ctx.message.add_reaction(self.bot.icons['greentick'])
            self.bot.status = ""

    @status.command(hidden=True)
    async def watching(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=3))
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @status.command(hidden=True)
    async def listening(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=2))
            await ctx.message.add_reaction(self.bot.icons['greentick'])
            self.bot.status = ""

    @status.command(hidden=True)
    async def competing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=5))
            await ctx.message.add_reaction(self.bot.icons['greentick'])
            self.bot.status = ""

    @status.command(aliases=["default", "original"], hidden=True)
    async def reset(self, ctx):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(self.bot.guilds)} guilds & {len(self.bot.users)} users"))
            self.bot.status = None
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @developer.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
        proc = await asyncio.create_subprocess_shell("git pull", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout:
            shell = f"[stdout]\n{stdout.decode()}"
        if stderr:
            shell = f"[stderr]\n{stderr.decode()}"
        em=discord.Embed(description=f"```sh\n$git pull\n{shell}```", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @developer.command(hidden=True)
    @commands.is_owner()
    async def prefix(self, ctx):
        self.bot.emptyPrefix = not self.bot.emptyPrefix
        if self.bot.emptyPrefix == True:
            em=discord.Embed(description="I've enabled empty prefix", color=color())
        else:
            em=discord.Embed(description="I've disabled empty prefix", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @developer.command(hidden=True, aliases=["rs"])
    @commands.is_owner()
    async def restart(self, ctx):
        em=discord.Embed(description="Are you sure you want to execute this command?", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)
        reactions = [self.bot.icons['greentick'], self.bot.icons['redtick']]
        for reaction in reactions:
            await msg.add_reaction(reaction)
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in reactions and reaction.message == msg)
        if str(reaction.emoji) == self.bot.icons['greentick']:
            for reaction_ in reactions:
                try:
                    await msg.clear_reactions()
                except Exception:
                    pass
            em=discord.Embed(description=f"Now restarting... {self.bot.icons['loading']}", color=color())
            await msg.edit(embed=em)
            for i in list(self.bot.directorys):
                self.bot.directorys[i].cleanup()
            await self.bot.db.close()
            await self.bot.session.close()
            await self.bot.close()
        elif str(reaction.emoji) == self.bot.icons['redtick']:
            await msg.delete()

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.is_owner()
    async def pip(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command.name})

    @pip.command(hidden=True, aliases=["add"])
    @commands.is_owner()
    async def install(self, ctx, *, package):
        if pwd.getpwuid(os.getuid())[0] == "pi":
            code = codeblock_converter(f"pip3.9 install {package}")
            await ctx.invoke(self.bot.get_command("jishaku shell"), **{"argument": code})
        else:
            code = codeblock_converter(f"python3.9 -m pip install {package}")
            await ctx.invoke(self.bot.get_command("jishaku shell"), **{"argument": code})

    @pip.command(hidden=True, aliases=["remove", "delete"])
    @commands.is_owner()
    async def uninstall(self, ctx, *, package):
        if pwd.getpwuid(os.getuid())[0] == "pi":
            code = codeblock_converter(f"pip3.9 uninstall -y {package}")
            await ctx.invoke(self.bot.get_command("jishaku shell"), **{"argument": code})
        else:
            code = codeblock_converter(f"python3.9 -m pip uninstall -y {package}")
            await ctx.invoke(self.bot.get_command("jishaku shell"), **{"argument": code})

    @developer.command(aliases=["eval", "e"])
    @commands.is_owner()
    async def evaluate(self, ctx, *, code : codeblock_converter):
        await ctx.invoke(self.bot.get_command("jishaku python"), **{"argument": code})

    @developer.command(aliases=["cmdus", "cmdusage", "commandus"])
    @commands.is_owner()
    async def commandusage(self, ctx, *, command : str = None):
        if command is None:

            if len(list(self.bot.command_usage)) == 0 and list(self.bot.command_usage) == []:
                em=discord.Embed(description="N/A", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                res = WrapList(list(self.bot.command_usage), 6)
                embeds = []
                for txt in res:
                    em=discord.Embed(title="Command Usage", description="\n".join(f"`{text}` - `{self.bot.command_usage[text]['usage']}`" for text in txt), color=color())
                    embeds.append(em)
                pag = menus.MenuPages(Paginator(embeds, per_page=1))
                await pag.start(ctx)

        else:
            
            command = self.bot.get_command(command)

            if command is None:
                return await ctx.reply(f"That command doesn't exist", mention_author=False)

            if command.parent is not None:
                command_name = f"{command.parent.name} {command.name}"
            else:
                command_name = command.name

            try:
                cmd = self.bot.command_usage[command_name]
            except KeyError:
                print(self.bot.command_usage)
                return await ctx.reply(f"I could not find any stats for `{command_name}`", mention_author=False)
            em=discord.Embed(
                title=command_name,
                description=f"`{command_name}` - `{cmd['usage']}`",
                color=color()
            )
            await ctx.reply(embed=em, mention_author=False)


    @commands.group(aliases=["sim"], invoke_without_command=True, description="A command to dispatch events")
    @commands.is_owner()
    async def simulate(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command":ctx.command.name})

    @simulate.command()
    @commands.is_owner()
    async def message(self, ctx, member : discord.Member, *, message : str):
        msg: discord.Message = copy.copy(ctx.message)
        msg.author = member
        msg.channel = ctx.channel
        msg.content = message
        self.bot.dispatch("message", msg)
        await ctx.message.add_reaction(self.bot.icons["greentick"])

    @simulate.command()
    @commands.is_owner()
    async def delete(self, ctx, member : discord.Member, *, message : str):
        msg: discord.Message = copy.copy(ctx.message)
        msg.author = member
        msg.channel = ctx.channel
        msg.content = message
        self.bot.dispatch("message_delete", msg)
        await ctx.message.add_reaction(self.bot.icons["greentick"])

    @simulate.command()
    @commands.is_owner()
    async def join(self, ctx):
        self.bot.dispatch("guild_join", ctx.guild)
        await ctx.message.add_reaction(self.bot.icons["greentick"])

    @simulate.command(aliases=["remove"])
    @commands.is_owner()
    async def leave(self, ctx):
        self.bot.dispatch("guild_remove", ctx.guild)
        await ctx.message.add_reaction(self.bot.icons["greentick"])

    @developer.command(hidden=True)
    @commands.is_owner()
    async def sql(self, ctx, *, query):
        res = await self.bot.db.fetch(query)
        if len(res) == 0:
            await ctx.message.add_reaction(self.bot.icons['greentick'])
        else:
            headers = list(res[0].keys())
            table = PrettyTable()
            table.field_names = headers
            for rec in res:
                lst = list(rec)
                table.add_row(lst)
            msg = table.get_string()
            await ctx.send(f"```\n{msg}\n```")

def setup(bot):
    bot.add_cog(Admin(bot))
