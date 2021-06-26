from attr import has
import discord, difflib, asyncio, traceback, aiohttp
from jishaku.models import copy_context_with
from discord.ext import commands
from utils.webhook import Webhook, AsyncWebhookAdapter
from utils.checks import is_mod
from utils.get import * 
from utils.errors import *

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.content != before.content:
            await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if not msg.author.bot and msg.guild is not None:
            res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
            try:
                commands = res["commands"]
            except TypeError:
                commands = ""
            commands = commands.split(",")
            if "snipe" in commands:
                return
            self.bot.message_cache[msg.guild.id] = {}
            self.bot.message_cache[msg.guild.id][msg.channel.id] = msg
            await asyncio.sleep(10)
            try:
                message = self.bot.message_cache[msg.guild.id][msg.channel.id]
            except Exception:
                pass
            else:
                if message == msg:
                    self.bot.message_cache[msg.guild.id].pop(msg.channel.id)
                    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if ctx.command is not None:
            if hasattr(ctx.command, "on_error"):
                return

            if hasattr(self.bot.get_cog(ctx.command.cog_name), "on_error"):
                return

        if isinstance(error, TooLong):
            await ctx.reply(f"{self.bot.icons['redtick']} {error}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        if isinstance(error, NotFound):
            await ctx.reply(f"{self.bot.icons['redtick']} {error}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            
        elif isinstance(error, commands.CommandOnCooldown):
            if not is_mod(self.bot, ctx.author):
                await ctx.reply(f"{self.bot.icons['redtick']} This command is on cooldown, try again in `{round(error.retry_after, 1)}` seconds", mention_author=False)
            else:
                await ctx.reinvoke()

        elif isinstance(error, commands.MissingRequiredArgument):
            param = str(error.param).split(":")
            param = param[0].replace(" ", "")
            await ctx.reply(f"`{self.bot.icons['redtick']} {param}` is a required argument that is missing", mention_author=False)

        elif isinstance(error, commands.CommandNotFound):
            if ctx.prefix != "":
                cmd = ctx.invoked_with
                cmds = [cmd.name for cmd in self.bot.commands]
                match = difflib.get_close_matches(cmd, cmds)
                try:
                    command = self.bot.get_command(match[0])
                except IndexError:
                    command = None
                if command:
                    if not command.hidden:
                        msg = await ctx.send(f"{self.bot.icons['redtick']} `{cmd}` is not a valid command, did you mean `{match[0]}`?", delete_after=5)
                        reactions = [self.bot.icons['greentick'], self.bot.icons['redtick']]
                        for reaction in reactions:
                            await msg.add_reaction(reaction)

                        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in reactions and reaction.message == msg)
                        if str(reaction.emoji) == self.bot.icons['greentick']:
                            args = ctx.message.content.removeprefix(f"{ctx.prefix}{cmd}")
                            alt_ctx = await copy_context_with(ctx, author=ctx.author, content=f"{ctx.prefix}{match[0]}{args}")
                            await self.bot.invoke(alt_ctx)
                            await msg.delete()
                        elif str(reaction.emoji) == self.bot.icons['redtick']:
                            await msg.delete()
                else:
                    em=discord.Embed(description=f"`{cmd}` is not a valid command", color=self.bot.color)
                    m = await ctx.reply(embed=em, mention_author=False, delete_after=3)

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(f"{self.bot.icons['redtick']} This command can only be executed in nsfw marked channels")

        elif isinstance(error, commands.MemberNotFound):
            em=discord.Embed(description=f"{self.bot.icons['redtick']} Couldn't find member `{error.argument}`", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

        elif isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(perm.replace("_", " ").lower() for perm in error.missing_perms)
            em=discord.Embed(description=f"{self.bot.icons['redtick']} I require `{perms}` permissions to execute this command", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

        elif isinstance(error, commands.MissingPermissions):
            perms = ", ".join(perm.replace("_", " ").lower() for perm in error.missing_perms)
            em=discord.Embed(description=f"{self.bot.icons['redtick']} You're missing `{perms}` permissions to execute this command", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

        elif isinstance(error, commands.NotOwner):
            if list(error.args) != [] and len(list(error.args)) != 0:
                msg = list(error.args)[0]
                return await ctx.send(f"{self.bot.icons['redtick']} {msg}")
            await ctx.send(f"{self.bot.icons['redtick']} Only the bots owner is allowed to execute this command")

        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, TooLong):
                await ctx.reply(f"{self.bot.icons['redtick']} {error}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

            if isinstance(error, NotFound):
                await ctx.reply(f"{self.bot.icons['redtick']} {error}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

            elif isinstance(error, aiohttp.ClientConnectionError):
                address = f"{error.host}:{error.port}"
                em=discord.Embed(description=f"I couldn't connect to `{address}`", color=self.bot.color)
                await ctx.reply(embed=em, mention_author=False)

            elif isinstance(error, aiohttp.InvalidURL):
                await ctx.reply("Invalid URL", mention_author=False)

            elif isinstance(error, commands.BotMissingPermissions):
                perms = ", ".join(perm.replace("_", " ").lower() for perm in error.missing_perms)
                em=discord.Embed(description=f"I need {perms} permissions to execute this command", color=self.bot.color)
                await ctx.reply(embed=em, mention_author=False)

            elif isinstance(error, discord.Forbidden):
                await ctx.reply(f"{self.bot.icons['redtick']} I don't have permission to do this", mention_author=False)
            else:
                if is_mod(self.bot, ctx.author):
                    errormsg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                    try:
                        await ctx.reply(f"```py\n{errormsg}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
                    except Exception:
                        raise error
                    else:
                        raise error
                else:
                    em=discord.Embed(description=f"```py\n{error}```", color=self.bot.color)
                    await ctx.reply(embed=em, mention_author=False)
                    raise error

        else:
            if is_mod(self.bot, ctx.author):
                errormsg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                try:
                    await ctx.reply(f"```py\n{errormsg}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
                except Exception:
                    raise error
                else:
                    raise error
            else:
                em=discord.Embed(description=f"```py\n{error}```", color=self.bot.color)
                await ctx.reply(embed=em, mention_author=False)
                raise error

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild.id != 336642139381301249:
            return

        role = after.guild.premium_subscriber_role
        if not role in before.roles and role in after.roles:
            channel = after.guild.get_channel(381963689470984203)
            em=discord.Embed(description=f"{self.bot.icons['vibecat']} {after.mention} has just boosted the server {await self.bot.roo(self.bot).pog()}", color=self.bot.color)
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        webhook = Webhook.from_url(str(self.bot.config["LOGS"]), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Join Guild", description=f"""
{self.bot.icons['arrow']}Name: `{guild.name}`
{self.bot.icons['arrow']}Members: `{guild.member_count}`
{self.bot.icons['arrow']}Owner: `{guild.owner}` ({guild.owner.id})
""", color=self.bot.color)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=f"ID: {guild.id}")
        await webhook.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        webhook = Webhook.from_url(str(self.bot.config["LOGS"]), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Leave Guild", description=f"""
{self.bot.icons['arrow']}Name: `{guild.name}`
{self.bot.icons['arrow']}Members: `{guild.member_count}`
{self.bot.icons['arrow']}Owner: `{guild.owner}` ({guild.owner.id})
""", color=self.bot.color)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=f"ID: {guild.id}")
        await webhook.send(embed=em)
 
    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            msg = await self.bot.wait_for("message", check=lambda msg: msg.author == self.bot.user and msg.reference.resolved == ctx.message)
        except Exception:
            pass
        else:
            await self.bot.wait_for("message_delete", check=lambda msg: msg == ctx.message) 
            await msg.delete()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.cmdsSinceRestart += 1
        command_name = None
        if ctx.command.parent is not None:
            command_name = f"{ctx.command.parent.name} {ctx.command.name}"
        else:
            command_name = ctx.command.name
        try:
            command = self.bot.command_usage[command_name]
        except KeyError:
            self.bot.command_usage[command_name] = {"usage": 1}
        else:
            self.bot.command_usage[command_name] = {"usage": command["usage"]+1}



def setup(bot):
    bot.add_cog(Errors(bot))
