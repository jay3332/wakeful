import discord, os, datetime, json, asyncio
from discord.ext import commands, tasks
from colorama import Fore
from discord.ext.commands.bot import when_mentioned_or
from discord.flags import Intents
from utils.configs import color
from utils.checks import is_blacklisted, is_mod

async def get_prefix(bot, message):
    await bot.wait_until_ready()
    if message.guild is None:
        return when_mentioned_or("!")
    else:
        with open("prefixes.json", "r") as f:
            prefixees = json.load(f)
        try:
            prefix = prefixees[str(message.guild.id)]
        except KeyError:
            prefixees[str(message.guild.id)] = "w,"
            with open("prefixes.json", "w") as f:
                json.dump(prefixees, f, indent=4)
        return prefixees[str(message.guild.id)]

devprefix = "." # the prefix for the development version

if os.getlogin() == "pi":
    bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
else:
    bot = commands.AutoShardedBot(command_prefix=devprefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
bot.remove_command("help")

with open('config.json') as f:
    conf = json.load(f)

bot.uptime = datetime.datetime.utcnow()
token = conf["TOKEN"]
devtoken = conf["DEVTOKEN"]
bot.github = "https://github.com/pvffyn/wakeful" # the github the bot is hosted on
bot.suggestions = conf["SUGGESTIONS"] # this will be used as a webhook for suggestions
bot.greenTick="✓"
bot.redTick="x"
bot.error="!"
bot.status = None
bot.guild = int(conf["GUILD"]) # your bots support server
bot.mod_role = int(conf["MODROLE"]) # moderator role on your bots support server
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

@tasks.loop(seconds=10)
async def presence():
    await asyncio.sleep(2)
    if bot.status == None:
        await bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(bot.guilds)} guilds & {len(bot.users)} users"))
    else:
        pass

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if is_blacklisted(msg.author):
        return
    elif os.getlogin() == "pi":
        if msg.content.startswith(await get_prefix(bot, msg)):
            await bot.process_commands(msg)
        elif msg.content == f"<@!{bot.user.id}>" or msg.content == f"<@{bot.user.id}>":
            if msg.guild:
                em=discord.Embed(description=f"the prefix for `{msg.guild.name}` is `{await get_prefix(bot, msg)}`", color=color())
                await msg.channel.send(embed=em)
            else:
                em=discord.Embed(description=f"the prefix for dms is `{await get_prefix(bot, msg)}`", color=color())
                await msg.channel.send(embed=em)
    elif msg.content == f"<@!{bot.user.id}>" or msg.content == f"<@{bot.user.id}>":
        if is_mod(bot, msg.author):
            em=discord.Embed(description=f"my prefix is `{devprefix}`", color=color())
            await msg.channel.send(embed=em)
    elif msg.content.startswith(devprefix):
        if is_mod(bot, msg.author):
            await bot.process_commands(msg)

@bot.event
async def on_ready():
    os.system("clear")
    print(f"Logged in as: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        if not filename[:-3] == "template":
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{Fore.GREEN}cogs.{filename[:-3]} has been succesfully loaded{Fore.RESET}")
            except:
                print(f"{Fore.RED}An error occured while loading cogs.{filename[:-3]}{Fore.RESET}")

bot.load_extension("jishaku")
presence.start()
if os.getlogin() == "pi": # check if username is pi
    bot.run(token) # run stable
else:
    bot.run(devtoken) # run development version
