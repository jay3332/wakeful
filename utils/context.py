import discord
import asyncio
import typing
from discord.ext import commands

class SusContext(commands.Context):

    async def send(self, content=None, *args, **kwargs):

        allowed_mentions = kwargs.pop("allowed_mentions", None)

        try:
            if allowed_mentions is None:
                return await self.reply(content=content, mention_author=False, allowed_mentions=discord.AllowedMentions.none(), *args, **kwargs)
            else:
                return await self.reply(content=content, mention_author=False, *args, **kwargs)
        except discord.NotFound:
            return await super().reply(content=content, *args, **kwargs)

    class processing:
        __slots__ = ("ctx", "delete_after", "m")

        def __init__(self, ctx, delete_after: bool = True):
            self.ctx = ctx
            self.delete_after = delete_after
            self.m = None

        async def __aenter__(self, *args: typing.List[typing.Any], **kwargs):
            self.m = await asyncio.wait_for(self.ctx.send(f"{self.ctx.bot.icons['loading']} Processing command, please wait..."), timeout=3.0)
            await self.ctx.trigger_typing()
            return self

        async def __aexit__(self, *args, **kwargs):
            if self.delete_after:
                try:
                    await self.m.delete()
                except discord.HTTPException:
                    return