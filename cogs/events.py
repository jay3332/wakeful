import discord, difflib, asyncio, traceback
from colorama import Fore
from jishaku.models import copy_context_with
from discord.ext import commands
from utils.webhook import Webhook, AsyncWebhookAdapter
from utils.checks import is_mod
from utils.get import * 

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if not msg.author.bot:
            self.bot.message_cache[msg.guild.id] = {}
            self.bot.message_cache[msg.guild.id][msg.channel.id] = msg
            await asyncio.sleep(10)
            if self.bot.message_cache[msg.guild.id][msg.channel.id] == msg:
                self.bot.message_cache[msg.guild.id].pop(msg.channel.id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if not is_mod(self.bot, ctx.author):
                em=discord.Embed(description=f"This command is on cooldown, try again in `{round(error.retry_after, 1)}` seconds.", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                ctx.command.reset_cooldown(ctx)
                await self.bot.process_commands(ctx.message)
        elif isinstance(error, commands.MissingRequiredArgument):
            param = str(error.param).split(":")
            param = param[0].replace(" ", "")
            em=discord.Embed(description=f"`{param}` is a required argument that is missing", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.bot.commands]
            match = difflib.get_close_matches(cmd, cmds)
            try:
                command = self.bot.get_command(match[0])
            except IndexError:
                command = None
            if command:
                if not command.hidden:
                    em=discord.Embed(description=f"`{cmd}` is not a valid command, did you mean `{match[0]}`?", color=color())
                    msg = await ctx.reply(embed=em, mention_author=False, delete_after=5)
                    reactions = [self.bot.icons['greentick'], self.bot.icons['redtick']]
                    for reaction in reactions:
                        await msg.add_reaction(reaction)
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in reactions and reaction.message == msg)
                    if str(reaction.emoji) == self.bot.icons['greentick']:
                        alt_ctx = await copy_context_with(ctx, author=ctx.author, content=f"{ctx.prefix}{match[0]}")
                        await self.bot.invoke(alt_ctx)
                    elif str(reaction.emoji) == self.bot.icons['redtick']:
                        await msg.delete()
            else:
                em=discord.Embed(description=f"`{cmd}` is not a valid command", color=color())
                m = await ctx.reply(embed=em, mention_author=False, delete_after=3)
        elif isinstance(error, commands.MemberNotFound):
            em=discord.Embed(description=f"Couldn't find member `{error.argument}`", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.BotMissingPermissions):
            em=discord.Embed(description=f"I don't have permission to do this", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.MissingPermissions):
            em=discord.Embed(description=f"You don't have permission to do this", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.MissingAnyRole):
            em=discord.Embed(description=f"You don't have permission to do this", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.NotOwner):
            if list(error.args) != [] and len(list(error.args)) != 0:
                msg = list(error.args)[0]
                em=discord.Embed(description=msg, color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description="You aren't allowed to execute this command", color=color())
                await ctx.reply(embed=em, mention_author=False)
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, discord.Forbidden):
                em=discord.Embed(description=f"I don't have permission to do this", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                if is_mod(self.bot, ctx.author):
                    errormsg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                    await ctx.reply(f"```py\n{errormsg}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
                else:
                    em=discord.Embed(description=f"```py\n{error}```", color=color())
                    await ctx.reply(embed=em, mention_author=False)
                raise error
        else:
            if is_mod(self.bot, ctx.author):
                errormsg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                await ctx.reply(f"```py\n{errormsg}```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            else:
                em=discord.Embed(description=f"```py\n{error}```", color=color())
            await ctx.reply(embed=em, mention_author=False)
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        webhook = Webhook.from_url(str(get_config("LOGS")), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Join Guild", description=f"""
{self.bot.icons['arrow']}Name: `{guild.name}`
{self.bot.icons['arrow']}Members: `{guild.member_count}`
{self.bot.icons['arrow']}Owner: `{guild.owner}`
""", color=color())
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=f"ID: {guild.id}")
        await webhook.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        webhook = Webhook.from_url(str(get_config("LOGS")), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Leave Guild", description=f"""
{self.bot.icons['arrow']}Name: `{guild.name}`
{self.bot.icons['arrow']}Members: `{guild.member_count}`
{self.bot.icons['arrow']}Owner: `{guild.owner}`
""", color=color())
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=f"ID: {guild.id}")
        await webhook.send(embed=em)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.cmdsSinceRestart += 1



def setup(bot):
    bot.add_cog(Errors(bot))
