from discord.mentions import AllowedMentions
from utils.errors import TooLong
from utils.checks import gameRunning
import discord, io, asyncdagpi, asyncio, datetime, string, random, json, wonderwords, typing
from discord.ext import commands
from fuzzywuzzy import fuzz
from gtts import gTTS
from jishaku.functools import executor_function
from utils.get import *
from utils.functions import *
from akinator.async_aki import Akinator
from cogs.music import is_vc
from cogs.utility import cleanup, make

dagpi = asyncdagpi.Client(get_config("DAGPI"))
akin = Akinator()

@executor_function
def do_tts(message):
    array = io.BytesIO()
    tts = gTTS(text=message, lang="en")
    tts.write_to_fp(array)
    array.seek(0)
    return array

@executor_function
def vctts(message, path):
    res = gTTS(text=message, lang="en")
    res.save(f"{path.name}/file.wav")

@executor_function
def typeracer(img, sentence):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("data/font.ttf", 150)
    draw.text((0, 0),str(sentence),(0,0,0),font=font)
    array = io.BytesIO()
    img.save(array, format="png")
    return discord.File(io.BytesIO(array.getvalue()), "typeracer.png")

class Fun(commands.Cog):

    """Fun & games commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *, message):
        if len(message) > 500:
            raise TooLong("The text can't be over 500 characters long")
        async with ctx.typing():
            file = await do_tts(message)
        await ctx.reply(file=discord.File(file, f"{message}.wav"), mention_author=False)

    @commands.group(aliases=["vctts"], invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def voicechattts(self, ctx, *, message):
        if len(message) > 500:
            raise TooLong("The text can't be over 500 characters long")
            
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            return await ctx.reply(embed=em, mention_author=False)

        path = await make()

        async with ctx.typing():
            await vctts(message, path)

        try:
            await ctx.author.voice.channel.connect()
        except AttributeError:
            em=discord.Embed(description="You have to join a voice channel to use this command", color=color())
            return await ctx.reply(embed=em, mention_author=False)
        except discord.ClientException:
            pass
        else:
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{path.name}/file.wav"), volume=100)
        
        try:
            ctx.voice_client.play(source, after=lambda e: '')
        except discord.ClientException as exc:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            return await ctx.reply(str(exc), mention_author=False, AllowedMentions=discord.AllowedMentions.none())

        await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command(aliases=["pick"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def choose(self, ctx, *options):
        await ctx.reply(random.choice(options), mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @voicechattts.command(name="stop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _stop(self, ctx):
        if not is_vc(ctx, ctx.author) and ctx.voice_client is not None:
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            return await ctx.reply(embed=em, mention_author=False)

        if not ctx.voice_client.is_playing():
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"I am currently not playing anything", color=color())
            return await ctx.reply(embed=em, mention_author=False)

        ctx.voice_client.stop()
        await ctx.message.add_reaction(self.bot.icons["greentick"])
    
    @commands.command(aliases=["aki"])
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def akinator(self, ctx):
        if gameRunning(ctx, ctx.command.name):
            channel = self.bot.games[ctx.command.name][str(ctx.guild.id)]["channel"]
            message = self.bot.games[ctx.command.name][str(ctx.guild.id)]["message"]
            em=discord.Embed(description=f"There is already a game of {ctx.command.name} running in {channel.mention}, click [here]({message.jump_url}) to look at it", color=color())
            return await ctx.reply(embed=em, mention_author=False)

        controls = {
            "yes": self.bot.icons['greentick'],
            "no": self.bot.icons['redtick'],
            "idk": self.bot.icons['shrug'],
        }

        emojis = [controls[e] for e in list(controls)]

        em=discord.Embed(description=f"{self.bot.icons['loading']} Now starting the game...", color=color())
        msg = await ctx.reply(embed=em, mention_author=False)

        game = await akin.start_game()

        self.bot.games["akinator"][str(ctx.guild.id)] = {
            "channel": ctx.channel,
            "message": msg
        }

        while akin.progression <= 80:
            if round(akin.progression) == 0:
                em=discord.Embed(description=f"""
{game}
{controls['yes']} = Yes
{controls['no']} = No
{controls['idk']} = I don't know""", color=color())
                await msg.edit(embed=em)
            for emoji in list(controls):
                await msg.add_reaction(str(controls[emoji]))

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in emojis and reaction.message == msg)
            except asyncio.TimeoutError:
                em=discord.Embed(description="The game has been stopped as you've not been responding for 30 seconds", color=color())
                await msg.edit(embed=em)
                self.bot.games["akinator"].pop(str(ctx.guild.id))
                break
            else:
                if str(reaction.emoji) == controls["yes"]:
                    first_answer = "yes"
                elif str(reaction.emoji) == controls["no"]:
                    first_answer = "no"
                elif str(reaction.emoji) == controls["idk"]:
                    first_answer = "idk"

                question = await akin.answer(first_answer)

                em=discord.Embed(description=f"""
{question}
{controls['yes']} = Yes
{controls['no']} = No
{controls['idk']} = I don't know""", color=color())
                await msg.edit(embed=em)
        await akin.win()

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def age(self, ctx, name : typing.Union[discord.Member, str] = None):
        if name is None:
            name = ctx.author
        if isinstance(name, str):
            res = await self.bot.session.get(f"https://api.agify.io?name={name.replace(' ', '')}")
            res = await res.json()
            age = res["age"]
            em=discord.Embed(description=f"{name.title()}'s predicted age is {age}", color=color())
            em.set_footer(text=f"Powered by agify.io", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        elif isinstance(name, discord.Member):
            res = await self.bot.session.get(f"https://api.agify.io?name={name.name.replace(' ', '')}")
            res = await res.json()
            age = res["age"]
            em=discord.Embed(description=f"{name.mention}'s estimated age is {age}", color=color())
            em.set_footer(text=f"Powered by agify.io", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.group(name="together", invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _together(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command.name})
    
    @_together.command(aliases=["yt"])
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def youtube(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel.id
        except AttributeError:
            em=discord.Embed(description=f"You have to join a voice channel to use this command", color=color())
            await ctx.send(embed=em)
        else:
            link = await self.bot.together.create_link(voice_channel, ctx.command.name)
            em=discord.Embed(description=f"Click this [link]({link}) to enable {ctx.command.name} together", color=color())
            await ctx.send(embed=em)

    @_together.command()
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def poker(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel.id
        except AttributeError:
            em=discord.Embed(description=f"You have to join a voice channel to use this command", color=color())
            await ctx.send(embed=em)
        else:
            link = await self.bot.together.create_link(voice_channel, ctx.command.name)
            em=discord.Embed(description=f"Click this [link]({link}) to enable {ctx.command.name} together", color=color())
            await ctx.send(embed=em)

    @_together.command()
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def chess(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel.id
        except AttributeError:
            em=discord.Embed(description=f"You have to join a voice channel to use this command", color=color())
            await ctx.send(embed=em)
        else:
            link = await self.bot.together.create_link(voice_channel, ctx.command.name)
            em=discord.Embed(description=f"Click this [link]({link}) to enable {ctx.command.name} together", color=color())
            await ctx.send(embed=em)

    @_together.command()
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def betrayal(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel.id
        except AttributeError:
            em=discord.Embed(description=f"You have to join a voice channel to use this command", color=color())
            await ctx.send(embed=em)
        else:
            link = await self.bot.together.create_link(voice_channel, ctx.command.name)
            em=discord.Embed(description=f"Click this [link]({link}) to enable {ctx.command.name} together", color=color())
            await ctx.send(embed=em)

    @_together.command()
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fishing(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel.id
        except AttributeError:
            em=discord.Embed(description=f"You have to join a voice channel to use this command", color=color())
            await ctx.send(embed=em)
        else:
            link = await self.bot.together.create_link(voice_channel, ctx.command.name)
            em=discord.Embed(description=f"Click this [link]({link}) to enable {ctx.command.name} together", color=color())
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def gender(self, ctx, name : typing.Union[discord.Member, str] = None):
        if name is None:
            name = ctx.author
        if isinstance(name, str):
            res = await self.bot.session.get(f"https://api.genderize.io?name={name.replace(' ', '')}")
            res = await res.json()
            gender = res["gender"]
            em=discord.Embed(description=f"{name.title()}'s predicted gender is {gender}", color=color())
            em.set_footer(text=f"Powered by genderize.io", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        elif isinstance(name, discord.Member):
            res = await self.bot.session.get(f"https://api.genderize.io?name={name.name.replace(' ', '')}")
            res = await res.json()
            gender = res["gender"]
            em=discord.Embed(description=f"{name.mention}'s predicted gender is {gender}", color=color())
            em.set_footer(text=f"Powered by genderize.io", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=["country"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nation(self, ctx, name : typing.Union[discord.Member, str] = None):
        if name is None:
            name = ctx.author
        if isinstance(name, str):
            res = await self.bot.session.get(f"https://api.nationalize.io?name={name.replace(' ', '')}")
            res = await res.json()
            if res["country"] != []:
                nation = res["country"][0]["country_id"]
                em=discord.Embed(description=f"{name.title()}'s predicted nation is {nation}", color=color())
                em.set_footer(text=f"Powered by nationalize.io", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)
            else:
                em=discord.Embed(description=f"I could not predict `{name.title()}`'s nation", color=color())
                await ctx.send(embed=em)
        elif isinstance(name, discord.Member):
            res = await self.bot.session.get(f"https://api.nationalize.io?name={name.name.replace(' ', '')}")
            res = await res.json()
            if res["country"] != []:
                nation = res["country"][0]["country_id"]
                em=discord.Embed(description=f"{name.mention}'s predicted nation is {nation}", color=color())
                em.set_footer(text=f"Powered by nationalize.io", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)
            else:
                em=discord.Embed(description=f"I could not predict {name.mention}'s nation", color=color())
                await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def bored(self, ctx):
        res = await self.bot.session.get("https://www.boredapi.com/api/activity")
        res = await res.json()
        if res["link"] != "":
            em=discord.Embed(title="Here's an activity to do", description=res["activity"], color=color(), url=res["link"])
        else:
            em=discord.Embed(title="Here's an activity to do", description=res["activity"], color=color())
        em.set_footer(text=f"Powered by boredapi.com", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://reddit.com/r/memes/top.json")
            res = await res.json()
            amount = len(res["data"]["children"])
            meme = res["data"]["children"][random.randrange(0,amount)]["data"]
        if meme["pinned"] != True and meme["over_18"] != True and not "youtu" in meme["url"] and meme["is_video"] != True:
            title = meme["title"]
            url = meme["url"]
            permalink = meme["permalink"]
            upvotes = meme["ups"]
            comments = meme["num_comments"]
            em = discord.Embed(title=title, url=f"https://reddit.com{permalink}", color=color())
            em.set_footer(text=f"👍 {upvotes}• 💬 {comments}", icon_url=ctx.author.avatar_url)
            em.set_image(url=url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            await ctx.reinvoke()

    @commands.command(aliases=["typerace"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def typeracer(self, ctx):
        async with ctx.typing():
            start_time = datetime.datetime.utcnow()
            sentence = wonderwords.RandomSentence().sentence()
            img = await self.bot.session.get("https://media.discordapp.net/attachments/832746281335783426/850000934658244668/typeracer.jpg")
            _file = await typeracer(io.BytesIO(await img.read()), sentence)
            em=discord.Embed(description="First one to type this sentence wins", color=color())
            em.set_image(url="attachment://typeracer.png")
        _msg = await ctx.reply(embed=em, file=_file, mention_author=False)
        try:
            msg = await self.bot.wait_for("message", check=lambda message: fuzz.ratio(sentence, message.content) > 96 and message.channel == ctx.channel, timeout=60)
            delta = datetime.datetime.utcnow() - start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            em=discord.Embed(description=f"We have a winner! {msg.author.mention} has typed the sentence in `{seconds}` seconds", color=color())
            await msg.reply(embed=em, mention_author=False)
        except asyncio.TimeoutError:
            em=discord.Embed(description=f"No one sent the right sentence, it was `{sentence}`", color=color())
            await _msg.reply(embed=em)

    @commands.command(aliases=["gtl"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guessthelogo(self, ctx):
        async with ctx.typing():
            logo = await dagpi.logo()
            answer = logo.answer
            brand = logo.brand
            hint = logo.hint
            question = logo.question
            em = discord.Embed(description=f"Try guessing this logo in under 20 seconds - Hhint: ||`{hint}`||", color=color())
            em.set_image(url=question)
        emsg = await ctx.send(embed=em)
        try:
            brand = logo.brand
            msg = await self.bot.wait_for('message', check=lambda message: message.content.lower() == str(brand).lower() and message.channel == ctx.channel, timeout=20)
            em=discord.Embed(description=f"Correct! The logo was `{brand}`", color=color())
            em.set_thumbnail(url=logo.answer)
            await emsg.edit(embed=em)
        except asyncio.TimeoutError:
            em=discord.Embed(description=f"You took too long to answer, it was `{logo.brand}`", color=color())
            em.set_thumbnail(url=logo.answer)
            await emsg.edit(embed=em)
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def httpcat(self, ctx, code : int):
        res = await self.bot.session.get(f"https://http.cat/{code}")
        buf = io.BytesIO(await res.read())
        file=discord.File(buf, filename=f"{code}.png")
        em=discord.Embed(color=color())
        em.set_image(url=f"attachment://{code}.png")
        em.set_footer(text=f"Powered by http.cat", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em, file=file)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):
        async with ctx.typing():
            joke = await dagpi.joke()
            em = discord.Embed(description=joke, color=color())
            em.set_footer(text=f"Powered by dagpi.xyz", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="8ball")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        async with ctx.typing():
            response = await dagpi.eight_ball()
            em = discord.Embed(color=color())
            em.add_field(name="input", value=f"```\n{question}```", inline=False)
            em.add_field(name="output", value=f"```\n{response}```", inline=False)
            em.set_footer(text=f"Powered by dagpi.xyz", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roast(self, ctx):
        async with ctx.typing():
            roast = await dagpi.roast()
            em = discord.Embed(description=roast, color=color())
            em.set_footer(text=f"Powered by dagpi.xyz", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ppsize"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def pp(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s pp", description="8"+"".join("=" for x in range(random.randrange(0,10)))+"D", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def gayrate(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s gayrate", description=f"{member.name} is `{random.randrange(0,100)}`% gay", color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def caption(self, ctx, member : typing.Union[discord.Member, str] = None):
        url = await getImage(ctx, member)
        print(type(url))
        async with ctx.typing():
            res = await self.bot.session.post("https://captionbot.azurewebsites.net/api/messages", json={"Content": url, "Type": "CaptionRequest"}, headers={"Content-Type": "application/json; charset=utf-8"})
        text = await res.text()
        em=discord.Embed(description=text, color=color())
        em.set_image(url=url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="ascii")
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _ascii(self, ctx, *, text):
        text = text.replace(" ", "%20")
        async with ctx.typing():
            res = await self.bot.session.get(f"https://artii.herokuapp.com/make?text={text}")
            res = (await res.read()).decode()
        await ctx.reply(f"```{res}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        letters=[]
        for letter in text:
            if letter in string.ascii_letters:
                letters.append(letter)
            else:
                if letter == " ":
                    letters.append(" ")
        if letters != [] and len(letters) != 0:
            res = "".join(f":regional_indicator_{letter}:" if not letter == " " else " " for letter in letters)
            try:
                await ctx.reply(res, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            except discord.HTTPException:
                await ctx.reply(mention_author=False, file=getFile(res))
        else:
            em=discord.Embed(description="​I couldn't find any ascii letters in your text", color=color())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def advice(self, ctx):
        async with ctx.typing():
            res = await self.bot.session.get("https://api.adviceslip.com/advice")
        res = (await res.read()).decode()
        advice = (json.loads(res))["slip"]["advice"]
        em=discord.Embed(description=advice, color=color())
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def mock(self, ctx, *, msg : str = None):
        if msg is None:
            if ctx.message.reference:
                text = ctx.message.reference.resolved.clean_content
        else:
            text = msg
        await ctx.reply("".join(letter.lower() if random.choice([1,2]) == 2 else letter.upper() for letter in text), mention_author=False, allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(Fun(bot))
