import discord, difflib, asyncio
from colorama import Fore
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from utils.configs import color
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
            em=discord.Embed(description=f"`{error.param}` is a required argument that is missing", color=color())
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
                    em=discord.Embed(description=f"`{cmd}` is not a valid command, maybe you meant `{match[0]}`", color=color())
                    m = await ctx.reply(embed=em, mention_author=False)
                    await asyncio.sleep(3)
                    await m.delete()
            else:
                em=discord.Embed(description=f"`{cmd}` is not a valid command", color=color())
                m = await ctx.reply(embed=em, mention_author=False)
                await asyncio.sleep(3)
                await m.delete()
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
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, discord.Forbidden):
                em=discord.Embed(description=f"I don't have permission to do this", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"```{error}```", color=color())
                await ctx.reply(embed=em, mention_author=False)
                raise error
        else:
            em=discord.Embed(description=f"```{error}```", color=color())
            await ctx.reply(embed=em, mention_author=False)
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        webhook = Webhook.from_url(str(get_config("LOGS")), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Join Guild", description=f"""
Name: `{guild.name}`
ID: `{guild.id}`
Members: `{guild.member_count}`
Owner: `{guild.owner}`
""", color=color())
        em.set_thumbnail(url=guild.icon_url)
        await webhook.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        webhook = Webhook.from_url(str(get_config("LOGS")), adapter=AsyncWebhookAdapter(self.bot.session))
        em=discord.Embed(title="Leave Guild", description=f"""
Name: `{guild.name}`
ID: `{guild.id}`
Members: `{guild.member_count}`
Owner: `{guild.owner}`
""", color=color())
        em.set_thumbnail(url=guild.icon_url)
        await webhook.send(embed=em)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.cmdsSinceRestart += 1



def setup(bot):
    bot.add_cog(Errors(bot))
