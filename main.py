import discord, os, datetime, json, asyncio, aiohttp, pwd, asyncpg, logging, coloredlogs, discordTogether, random, string
from discord.ext.commands.bot import when_mentioned_or
from discord.ext import commands, tasks
from colorama import Fore
from utils import menus
from utils.checks import is_blacklisted, is_mod
from utils.get import *

with open('config.json') as f:
    conf = json.load(f)


async def get_prefix(bot, message):
    await bot.wait_until_ready()

    if message.author.id == bot.ownersid and bot.emptyPrefix == True:
        return commands.when_mentioned_or("")(bot, message)

    if message.guild is None:
        return commands.when_mentioned_or("!")(bot, message)
    else:
        try:
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return commands.when_mentioned_or(prefix["prefix"])(bot, message)
        except:
            if pwd.getpwuid(os.getuid())[0] != "pi":
                await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, ',w')
            else:
                await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, 'w,')
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return commands.when_mentioned_or(prefix["prefix"])(bot, message)

class wakeful(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime = datetime.datetime.utcnow()
        self.github = "https://github.com/jottew/wakeful" # the github the bot is hosted on
        self.invite = "https://discord.gg/RkCqvMJsDY"
        self.icons = conf["ICONS"]
        self.together = discordTogether.DiscordTogether(self)
        self.cmdsSinceRestart = 0
        self.message_cache = {}
        self.directorys = {}
        self.command_usage = {}
        self.roos = []
        self.games = {
            "akinator": {}
        }
        self.emptyPrefix = False
        self.ownersid = 797044260196319282
        self.afks = {}
        #self.banner = "https://media.discordapp.net/attachments/832746281335783426/849721738987307008/banner.png"
        self.session = aiohttp.ClientSession()
        self.status = None
        self.guild = int(conf["GUILD"])
        self.mod_role = int(conf["MODROLE"])

    def paginate(self, paginator):
        return menus.MenuPages(paginator)
    class roo():

        def __init__(self, bot):
            self.bot = bot

        def getEmoji(self, name : str):
            try:
                return self.bot.roos[name.lower()]
            except KeyError:
                return "didnt found find :anguished::anguished::anguished::anguished::anguished:"

        def __getattr__(self, attr):
            async def predicate():
                return self.getEmoji(attr)
            return predicate
        
    async def on_ready(self):
        logger.info(f"Logged in as: {bot.user} ({bot.user.id})")

        bot.roos = {em.name.lower().strip("roo"): str(em) for em in bot.emojis if em.name.lower().startswith("roo")}

    async def on_message(self, msg):
        if self.emptyPrefix and msg.author.id == self.ownersid:
            await self.process_commands(msg)
            return

        if pwd.getpwuid(os.getuid())[0] != "pi":
            if not is_mod(self, msg.author):
                return
        
        prefix = await get_prefix(self, msg)
        
        if msg.guild is None:
            if msg.content.startswith(prefix):
                return await msg.channel.send(f"DM commands are disabled, please invite me to a guild\nInvite: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=self\nSupport Server: {self.invite}")

        if msg.author.bot:
            return

        if await is_blacklisted(self, msg.author):
            return

        for i in prefix:
            if msg.content.startswith(i):
                    
                if msg.guild is not None:
                    try:
                        command = msg.content.split(i)
                    except ValueError:
                        command = msg.content
                    command = command[1]
                    res = await self.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
                    try:
                        commands = res["commands"]
                    except:
                        success = False
                    else:
                        success = True
                    if success:
                        command_obj = self.get_command(command)
                        try:
                            self.get_command(command).parent
                        except:
                            command_name = None
                        else:
                            command_name = "".join(command_obj.name if command_obj.parent is None else f"{command_obj.parent.name} {command_obj.name}")
                        commands = commands.split(",")
                        if command_name in commands and command != "":
                            if is_mod(self, msg.author):
                                pass
                            else:
                                em=discord.Embed(description=f"This command has been disabled by the server administrators", color=color())
                                return await msg.channel.send(embed=em)
                        else:
                            pass
                    else:
                        pass
                await self.process_commands(msg)
                return
            
            if msg.content == f"<@!{self.user.id}>" or msg.content == f"<@{self.user.id}>":
                if msg.guild:
                    em=discord.Embed(description=f"The prefix for `{msg.guild.name}` is `{prefix[2]}`", color=color())
                    return await msg.channel.send(embed=em)
                else:
                    em=discord.Embed(description=f"The prefix for dms is `{prefix[2]}`", color=color())
                    return await msg.channel.send(embed=em)

bot = wakeful(command_prefix=get_prefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
bot.remove_command("help")

token = conf["TOKEN"]
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

coloredlogs.install()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f"data/logs/discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@tasks.loop(seconds=10)
async def presence():
    await bot.wait_until_ready()
    if bot.status == None:
        await bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(bot.guilds)} guilds & {len(bot.users)} users"))
    else:
        pass

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"{Fore.GREEN}cogs.{filename[:-3]} has been succesfully loaded{Fore.RESET}")
        except Exception as exc:
            logger.info(f"{Fore.RED}An error occured while loading cogs.{filename[:-3]}{Fore.RESET}")
            raise exc

bot.load_extension("jishaku")
presence.start()
bot.db=bot.loop.run_until_complete(asyncpg.create_pool(host="localhost", port="5432", user=conf["dbuser"], password=conf["dbpw"], database="wakeful"))
bot.run(token) # run stable
