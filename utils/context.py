import discord
from discord.ext import commands

class SusContext(commands.Context):
    async def send(self, content=None, *args, **kwargs):

        return await self.reply(content=content, mention_author=False, *args, **kwargs)

    