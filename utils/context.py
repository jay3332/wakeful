import discord
from discord.ext import commands

class SusContext(commands.Context):
    async def send(self, content=None, *args, **kwargs):

        allowed_mentions = kwargs.pop("allowed_mentions", None)

        if allowed_mentions is None:
            return await self.reply(content=content, mention_author=False, allowed_mentions=discord.AllowedMentions.none(), *args, **kwargs)
        else:
            return await self.reply(content=content, mention_author=False, *args, **kwargs)
    