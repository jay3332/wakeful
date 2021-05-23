import discord, os, datetime, json, asyncio
from discord.ext import commands, tasks
from colorama import Fore
from discord.ext.commands.bot import when_mentioned_or
from discord.flags import Intents

bot = commands.Bot(command_prefix=when_mentioned_or(","), intents=discord.Intents.all())
bot.remove_command("help")

with open('config.json') as f:
    data = json.load(f)

bot.uptime = datetime.datetime.utcnow()
token = data["TOKEN"]
bot.github = "https://github.com/pvffyn/wakeful" # the github the bot is hosted on
bot.suggestions = data["SUGGESTIONS"] # this will be used as a webhook for suggestions
bot.greenTick="✓"
bot.redTick="x"
bot.error="!"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

@tasks.loop(seconds=10)
async def presence():
    await asyncio.sleep(2)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(f",help | {len(bot.guilds)} guilds & {len(bot.users)} users"))


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
bot.run(token)
