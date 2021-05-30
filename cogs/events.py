import discord, difflib, asyncio
from colorama import Fore
from discord.ext import commands
from utils.configs import color
from utils.checks import is_mod

class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if not is_mod(self.bot, ctx.author):
                embed=discord.Embed(description=f"this command is on cooldown, try again in `{round(error.retry_after, 1)}` seconds.", color=color())
                await ctx.send(embed=embed)
            else:
                ctx.command.reset_cooldown(ctx)
                await ctx.invoke(ctx.command)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=f"`{error.param}` is a required argument that is missing", color=color())
            await ctx.send(embed=embed)
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
                    embed=discord.Embed(description=f"`{cmd}` is not a valid command, maybe you meant `{match[0]}`", color=color())
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(3)
                    await m.delete()
            else:
                embed=discord.Embed(description=f"`{cmd}` is not a valid command", color=color())
                m = await ctx.send(embed=embed)
                await asyncio.sleep(3)
                await m.delete()
        elif isinstance(error, commands.MemberNotFound):
            embed=discord.Embed(description=f"could not find member `{error.argument}`", color=color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed=discord.Embed(description=f"i do not have permission to do this", color=color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(description=f"you do not have permission to do this", color=color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingAnyRole):
            embed=discord.Embed(description=f"you do not have permission to do this", color=color())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, discord.Forbidden):
                embed=discord.Embed(description=f"i do not have permission to do this", color=color())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(description=f"```{error}```", color=color())
                await ctx.send(embed=embed)
                raise error
        else:
            embed=discord.Embed(description=f"```{error}```", color=color())
            await ctx.send(embed=embed)
            raise error

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.cmdsSinceRestart += 1



def setup(bot):
    bot.add_cog(errors(bot))
