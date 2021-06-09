import discord, typing
from discord.ext import commands

class Paginator():

    def __init__(self, bot : typing.Union[discord.Client, commands.Bot], embeds : list, emojis : dict = {"full-left": "⏪", "left": "◀", "stop": "💠", "right": "▶", "full-right": "⏩"}):
        self.embeds = embeds
        self.pages = len(embeds)
        self.page = 0
        self.first_page = 0
        self.emojis = emojis
        self.reactions = [emojis[reaction] for reaction in list(emojis)]
        self.message = None
        self.bot = bot

    async def set_page(self, page : int):
        embeds = self.embeds
        await self.message.edit(embed=embeds[page])
        self.page = page

    async def stop(self):
        self.page = 1
        await self.message.clear_reactions()

    async def start(self, ctx):
        embeds = list(self.embeds)
        self.message = await ctx.send(embed=embeds[int(self.first_page)])
        for reaction in self.reactions:
            await self.message.add_reaction(reaction)
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) in self.reactions and user == ctx.author)
            try:
                await self.message.remove_reaction(str(reaction.emoji), user)
            except:
                pass
            if str(reaction.emoji) == self.emojis["full-left"]:
                page = self.first_page
                await self.set_page(page)
            elif str(reaction.emoji) == self.emojis["left"]:
                if self.page > 0:
                    self.page -= 1
                    await self.set_page(self.page)
            elif str(reaction.emoji) == self.emojis["stop"]:
                await self.stop()
            elif str(reaction.emoji) == self.emojis["right"]:
                self.page += 1
                await self.set_page(self.page)
            elif str(reaction.emoji) == self.emojis["full-right"]:
                page = self.pages-1
                await self.set_page(page)