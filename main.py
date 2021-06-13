from DiscordUtils.Music import Music
import discord, os, datetime, json, asyncio, aiohttp, pwd, asyncpg, logging, coloredlogs, discordTogether
from discord.ext.commands.bot import when_mentioned_or
from discord.ext import commands, tasks
from colorama import Fore
from discord.flags import Intents
from utils.checks import is_blacklisted, is_mod
from utils.get import *

with open('config.json') as f:
    conf = json.load(f)

devprefix = conf["DEVPREFIX"] # the prefix for the development version


async def get_prefix(bot, message):
    await bot.wait_until_ready()
    if message.author.id == bot.ownersid and bot.emptyPrefix == True:
        return ""
    if pwd.getpwuid(os.getuid())[0] != "pi":
        return devprefix
    if message.guild is None:
        return "!"
    else:
        try:
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return prefix["prefix"]
        except:
            await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, 'w,')
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return prefix["prefix"]


class wakeful(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    async def on_ready(self):
        logger.info(f"Logged in as: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")

bot = wakeful(command_prefix=get_prefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
bot.remove_command("help")

bot.uptime = datetime.datetime.utcnow()
token = conf["TOKEN"]
devtoken = conf["DEVTOKEN"]
bot.github = "https://github.com/jottew/wakeful" # the github the bot is hosted on
bot.invite = "https://discord.gg/RkCqvMJsDY"
bot.icons = conf["ICONS"]
bot.together = discordTogether.DiscordTogether(bot)
bot.cmdsSinceRestart = 0
bot.message_cache = {}
bot.directorys = {}
bot.emptyPrefix = False
bot.ownersid = 797044260196319282
bot.afks = {}
bot.banner = "https://media.discordapp.net/attachments/832746281335783426/849721738987307008/banner.png"
bot.session = aiohttp.ClientSession()
bot.status = None
bot.guild = int(conf["GUILD"]) # your bots support server
bot.mod_role = int(conf["MODROLE"]) # moderator role on your bots support server
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

@bot.event
async def on_message(msg):
    prefix = await get_prefix(bot, msg)
    
    if msg.guild is None:
        if msg.content.startswith(prefix):
            return await msg.channel.send(f"DM commands are disabled, please invite me to a guild\nInvite: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot\nSupport Server: {bot.invite}")

    if msg.author.bot:
        return

    if await is_blacklisted(bot, msg.author):
        return

    elif msg.content.startswith(prefix):
        if msg.guild is not None:
            try:
                command = msg.content.split(prefix)
            except ValueError:
                command = msg.content
            command = command[1]
            res = await bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
            try:
                commands = res["commands"]
            except:
                success = False
            else:
                success = True
            if success:
                command_obj = bot.get_command(command)
                try:
                    bot.get_command(command).parent
                except:
                    command_name = None
                else:
                    command_name = "".join(command_obj.name if command_obj.parent is None else f"{command_obj.parent.name} {command_obj.name}")
                commands = commands.split(",")
                if command_name in commands and command != "":
                    if is_mod(bot, msg.author):
                        pass
                    else:
                        em=discord.Embed(description=f"This command has been disabled by the server administrators", color=color())
                        await msg.channel.send(embed=em)
                        return
                else:
                    pass
            else:
                pass
        await bot.process_commands(msg)

    if msg.content == f"<@!{bot.user.id}>" or msg.content == f"<@{bot.user.id}>":
        if msg.guild:
            em=discord.Embed(description=f"The prefix for `{msg.guild.name}` is `{prefix}`", color=color())
            await msg.channel.send(embed=em)
        else:
            em=discord.Embed(description=f"The prefix for dms is `{prefix}`", color=color())
            await msg.channel.send(embed=em)

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
if pwd.getpwuid(os.getuid())[0] == "pi": # check if username is pi
    bot.run(token) # run stable
else:
    bot.run(devtoken) # run development version
