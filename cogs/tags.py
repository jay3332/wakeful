import discord, datetime, string, time, humanize
from discord.ext import commands
from utils.get import *

async def exists(ctx, name):
    res = await ctx.bot.db.fetchrow("SELECT * FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
    try:
        res = res["content"]
    except TypeError:
        return False
    else:
        return True

async def is_owner(ctx, name):
    res = await ctx.bot.db.fetchrow("SELECT * FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
    owner = int(res["author"])
    if ctx.author.id == owner:
        return True
    elif ctx.author.guild_permissions.manage_guild:
        return True
    else:
        return False

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Limit = 200
        self.MinLimit = 25

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def tag(self, ctx, *, name):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await self.bot.db.fetchrow("SELECT * FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
            name = tag["name"]
            content = tag["content"]
            await ctx.reply(content, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @tag.command(aliases=["info", "owner", "author"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def information(self, ctx, *, name):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await self.bot.db.fetchrow("SELECT * FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
            name = tag["name"]
            author = tag["author"]
            content = tag["content"]
            created = datetime.datetime.fromtimestamp(int(tag["created"]))# - datetime.timedelta(hours=2)
            if len(content) > self.MinLimit:
                exceeding = content[self.MinLimit:]
                content = content.replace(exceeding, "...")

            try:
                author = (ctx.guild.get_member(int(author))).mention
            except:
                author = "None"

            em=discord.Embed(title="", color=color())
            em.add_field(name="Name", value=name, inline=True)
            em.add_field(name="Author", value=author, inline=True)
            em.add_field(name="Content", value=content, inline=True)
            em.add_field(name="Created At", value=f"{created.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(created)})", inline=True)
            await ctx.reply(embed=em, mention_author=False)

    @tag.command(aliases=["update"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def edit(self, ctx, name, *, content):
        if len(content) > self.Limit:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The content can't be over 200 characters long", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("UPDATE tags SET content = $1 WHERE guild = $2 AND name = $3", content, ctx.guild.id, name)
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command(aliases=["delete", "del"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def remove(self, ctx, *, name):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("DELETE FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def rename(self, ctx, name, *, new_name):
        if await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is already a tag with the name `{name}`", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif len(new_name) < 3:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The new name has to be at least 3 characters long", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            valid_name = True
            for letter in new_name:
                if letter in list(string.punctuation):
                    valid_name = False

            if valid_name != True: # ---------------------------------- check if the name has any invalid characters
                await ctx.message.add_reaction(self.bot.icons['redtick'])
                em=discord.Embed(description=f"You can't have an unsupported character in the new name", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                await self.bot.db.execute("UPDATE tags SET name = $1 WHERE guild = $2 AND name = $3", new_name, ctx.guild.id, name)
                await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command(aliases=["make", "add"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def create(self, ctx, name, *, content):
        if await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is already a tag with the name `{name}`", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif len(name) < 3:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The new name has to be at least 3 characters long", color=color())
            await ctx.reply(embed=em, mention_author=False)
        elif len(content) > self.Limit:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The content can't be over 200 characters long", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            valid_name = True
            for letter in name:
                if letter in list(string.punctuation):
                    valid_name = False

            if valid_name != True: # ---------------------------------- check if the name has any invalid characters
                await ctx.message.add_reaction(self.bot.icons['redtick'])
                em=discord.Embed(description=f"You can't have an unsupported character in the new name", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                await self.bot.db.execute("INSERT INTO tags (guild, name, content, author, created) VALUES ($1, $2, $3, $4, $5)", ctx.guild.id, name, content, ctx.author.id, int(time.time()))
                await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def search(self, ctx, *, query):
        res = await self.bot.db.fetch("SELECT * FROM tags WHERE guild = $1", ctx.guild.id)
        records = []
        for record in res:
            if query in dict(record)["name"]:
                if len(records) < 6:
                    records.append(record)
        if records != [] and len(records) != 0:
            em=discord.Embed(title=f"Search: {query}", description="\n".join(f"`{dict(rec)['name']}`" for rec in records), color=color())
            em.set_footer(text=f"{len(res)} {''.join('record' if len(res) == 1 else 'records')} found")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"There are no tags with `{query}` in the name", color=color())
            await ctx.reply(embed=em, mention_author=False)



def setup(bot):
    bot.add_cog(Tags(bot))
