from utils.functions import getFile
import discord, datetime, string, time, humanize
from discord.ext import commands
from utils.get import *
from utils.paginator import *

async def exists(ctx, name):
    res = await ctx.bot.db.fetch("SELECT * FROM tags WHERE guild = $1", ctx.guild.id)
    tag = None
    for tag_ in res:
        if dict(tag_)["name"].lower() == name.lower():
            tag = tag_
    if tag is not None:
        return True
    else:
        return False

async def get_tag(ctx, name):
    res = await ctx.bot.db.fetch("SELECT * FROM tags WHERE guild = $1", ctx.guild.id)
    for tag in res:
        if dict(tag)["name"].lower() == name.lower():
            return tag

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
        self.Limit = 1250
        self.MinLimit = 25

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def tag(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            name = tag["name"]
            content = tag["content"]
            await ctx.reply(content, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @tag.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def raw(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            name = tag["name"]
            content = tag["content"]
            await ctx.reply(discord.utils.escape_markdown(content), mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @tag.command(aliases=["display", "view"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def show(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            name = tag["name"]
            content = tag["content"]
            await ctx.reply(content, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @tag.command(aliases=["info", "owner", "author"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def information(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            name = tag["name"]
            author_id = tag["author"]
            if len(tag["content"]) > self.MinLimit:
                content = tag["content"][:self.MinLimit-3]+"..."
            else:
                content = tag["content"]
            created = datetime.datetime.fromtimestamp(int(tag["created"]))

            try:
                author = (ctx.guild.get_member(int(author_id))).mention
            except Exception:
                author = "N/A"

            em=discord.Embed(title="", color=self.bot.color)
            em.add_field(name="Name", value=name, inline=True)
            em.add_field(name="Author", value=f"{author} ({author_id})", inline=True)
            em.add_field(name="Content", value=content, inline=True)
            em.add_field(name="Created At", value=f"{created.strftime('%d/%m/%Y at %H:%M:%S')} ({humanize.naturaltime(created)})", inline=True)
            await ctx.reply(embed=em, mention_author=False)

    @tag.command(aliases=["update"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def edit(self, ctx, name : commands.clean_content, *, content):
        if len(content) > self.Limit:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The content can't be over {self.Limit} characters long", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("UPDATE tags SET content = $1 WHERE guild = $2 AND name = $3", content, ctx.guild.id, name)
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command(aliases=["delete", "del"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def remove(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("DELETE FROM tags WHERE guild = $1 AND name = $2", ctx.guild.id, name)
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def rename(self, ctx, name : commands.clean_content, *, new_name : commands.clean_content):
        commands = [cmd.name for cmd in self.bot.get_command("tag").commands]
        for command in self.bot.get_command("tag").commands:
            for alias in command.aliases:
                commands.append(alias)
        if new_name in [cmd for cmd in commands]:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The tag name cannot be a tag subcommand", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif await exists(ctx, new_name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is already a tag with the name `{name}`", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif len(new_name) < 1:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The new name has to be at least 1 characters long", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("UPDATE tags SET name = $1 WHERE guild = $2 AND name = $3", new_name, ctx.guild.id, name)
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command(aliases=["make", "add"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def create(self, ctx, name : commands.clean_content, *, content):
        commands = [cmd.name for cmd in self.bot.get_command("tag").commands]
        for command in self.bot.get_command("tag").commands:
            for alias in command.aliases:
                commands.append(alias)
        if name in [cmd for cmd in commands]:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The tag name cannot be a tag subcommand", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is already a tag with the name `{name}`", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif len(name) < 1:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The name has to be at least 1 characters long", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif len(content) > self.Limit:
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"The content can't be over {self.Limit} characters long", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            await self.bot.db.execute("INSERT INTO tags (guild, name, content, author, created) VALUES ($1, $2, $3, $4, $5)", ctx.guild.id, name, content, ctx.author.id, int(time.time()))
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def claim(self, ctx, *, name : commands.clean_content):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            author = dict(tag)["author"]
            name_ = dict(tag)["name"]
            member = ctx.guild.get_member(int(author))
            if member is not None:
                await ctx.message.add_reaction(self.bot.icons['redtick'])
                em=discord.Embed(description=f"The tag owner is still on the server", color=self.bot.color)
                await ctx.reply(embed=em, mention_author=False)
            else:
                await self.bot.db.execute("UPDATE tags SET author = $1 WHERE guild = $2 AND name = $3", ctx.author.id, ctx.guild.id, name_)
                await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command(aliases=["give"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def transfer(self, ctx, name : commands.clean_content, member : discord.Member):
        if not await exists(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"There is no tag with the name `{name}` on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        elif not await is_owner(ctx, name):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"You don't own this tag", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)
        else:
            tag = await get_tag(ctx, name)
            name_ = dict(tag)["name"]
            await self.bot.db.execute("UPDATE tags SET author = $1 WHERE guild = $2 AND name = $3", member.id, ctx.guild.id, name_)
            await ctx.message.add_reaction(self.bot.icons['greentick'])
            await ctx.message.add_reaction(self.bot.icons['greentick'])

    @tag.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def search(self, ctx, *, query : commands.clean_content):
        res = await self.bot.db.fetch("SELECT * FROM tags WHERE guild = $1", ctx.guild.id)
        records = []
        for record in res:
            if query.lower() in dict(record)["name"].lower():
                records.append(record)
        if records != [] and len(records) != 0:
            res = WrapList(records, 6)
            embeds = []
            for txt in res:
                em=discord.Embed(description="\n".join(f"{list(records).index(text)+1}. {text['name']}" for text in txt), color=self.bot.color)
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            em=discord.Embed(description=f"There are no tags with `{query}` in the name", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

    @tag.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def all(self, ctx):
        records = sorted(await self.bot.db.fetch("SELECT * FROM tags WHERE guild = $1", ctx.guild.id))
        if records != [] and len(records) != 0:
            if ctx.message.content.endswith(" --txt"):
                text = "\n".join(f"{text['name']}" for text in records)
                return await ctx.reply(file=await getFile(text, filename="tags"), mention_author=False)

            res = WrapList(records, 6)
            embeds = []
            for txt in res:
                em=discord.Embed(description="\n".join(f"{list(records).index(text)+1}. {text['name']}" for text in txt), color=self.bot.color)
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            em=discord.Embed(description=f"There are no tags on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

    @tag.command(name="from", aliases=["by"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _from(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        records = sorted(await self.bot.db.fetch("SELECT * FROM tags WHERE guild = $1 AND author = $2", ctx.guild.id, member.id))
        if records != [] and len(records) != 0:
            res = WrapList(records, 6)
            embeds = []
            for txt in res:
                em=discord.Embed(description="\n".join(f"{list(records).index(text)+1}. {text['name']}" for text in txt), color=self.bot.color)
                em.set_author(name=member, icon_url=member.avatar_url)
                embeds.append(em)
            pag = self.bot.paginate(Paginator(embeds, per_page=1))
            await pag.start(ctx)
        else:
            em=discord.Embed(description=f"{member.mention} does not have any tags on this guild", color=self.bot.color)
            await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(Tags(bot))
