import discord, os, random, hashlib, datetime, json
from discord.ext import commands
from colorama import Fore
from discord.ext.commands.bot import when_mentioned_or
from discord.flags import Intents

bot = commands.Bot(command_prefix=when_mentioned_or(","), intents=discord.Intents.all())
bot.remove_command("help")
bot.uptime = datetime.datetime.utcnow()
bot.greenTick="✓"
bot.redTick="x"
bot.error="!"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"


presences=["yo momma fat", "me when the", "amogus SUS!!!!", "impoter", "trUmp fWon eLecetin!!!"]
@bot.event
async def on_ready():
    os.system("clear")
    presence = hashlib.sha256(random.choice(presences).encode()).hexdigest()
    print(f"Logged in as: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(presence))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        if not filename[:-3] == "template":
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{Fore.GREEN}cogs.{filename[:-3]} has been succesfully loaded{Fore.RESET}")
            except:
                print(f"{Fore.RED}An error occured while loading cogs.{filename[:-3]}{Fore.RESET}")
                

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]

bot.load_extension("jishaku")
bot.run(token)