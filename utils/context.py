import discord, asyncio, typing
from discord.ext import commands

class SusContext(commands.Context):
    async def send(self, content=None, *args, **kwargs):

        allowed_mentions = kwargs.pop("allowed_mentions", None)

        if allowed_mentions is None:
            return await self.reply(content=content, mention_author=False, allowed_mentions=discord.AllowedMentions.none(), *args, **kwargs)
        else:
            return await self.reply(content=content, mention_author=False, *args, **kwargs)

    class processing:
        __slots__ = ("ctx", "done", "m")

        def __init__(self, ctx):
            self.ctx = ctx
            self.done = False
            self.m = None

        async def __aenter__(self, *args: typing.List[typing.Any], **kwargs):
            self.m = await asyncio.wait_for(self.ctx.send(f"{self.ctx.bot.icons['loading']} Processing command, please wait..."), timeout=3.0)
            await self.ctx.trigger_typing()
            return self

        async def __aexit__(self, *args, **kwargs):
            try:
                await self.m.delete()
            except discord.HTTPException:
                return
            self.done = True
    