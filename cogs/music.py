import tempfile
import discord, DiscordUtils, humanize, re, asyncio, datetime
from discord.ext import commands
from utils.get import *
from jishaku.models import copy_context_with

def is_vc(ctx : commands.Context, member : discord.Member):
    if member.guild_permissions.manage_guild:
        return True
    if ctx.guild.me.voice is None:
        return True
    elif member.voice is None:
        return False
    elif ctx.guild.me.voice.channel == member.voice.channel:
        return True
    else:
        return False

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = DiscordUtils.Music()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            if guild.voice_client is not None:
                await guild.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.voice_client is not None and member.guild.me.voice is not None:
            if member == self.bot.user and before.deaf == True and after.deaf == False:
                await member.guild.me.edit(deafen=True)
            elif before.channel is not None and after.channel is None:
                if before.channel == member.guild.me.voice.channel:
                    members = [m for m in member.guild.me.voice.channel.members if not m.bot]
                    if members == [] and len(members) == 0:
                        await member.guild.voice_client.disconnect()

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except AttributeError:
            em=discord.Embed(description="You have to join a voice channel to use this command", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            await ctx.guild.me.edit(deafen=True)

    @commands.command()
    async def leave(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            await ctx.voice_client.disconnect()
            await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, url):
        if re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url):
            if not re.search(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$", url):
                em=discord.Embed(description="That is not a valid youtube video url", color=color())
                return await ctx.reply(embed=em, mention_author=False)
            else:
                pass
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            async with ctx.typing():
                try:
                    player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
                except DiscordUtils.NotConnectedToVoice:
                    try:
                        await ctx.author.voice.channel.connect()
                    except AttributeError:
                        em=discord.Embed(description="You have to join a voice channel to use this command", color=color())
                        return await ctx.reply(embed=em, mention_author=False)
                    else:
                        try:
                            await ctx.guild.me.edit(deafen=True)
                        except Exception:
                            pass
                        player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)

            if not ctx.voice_client.is_playing():
                await player.queue(url, search=True)
                await player.play()
            else:
                await player.queue(url, search=True)
            await ctx.message.add_reaction(self.bot.icons["greentick"])
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) == self.bot.icons['info']  and reaction.message == ctx.message and not user.bot and user == ctx.author, timeout=15)
            except asyncio.TimeoutError:
                pass
            else:
                alt_ctx = await copy_context_with(ctx, author=user, content=f"{ctx.prefix}nowplaying")
                await self.bot.invoke(alt_ctx)

    @commands.command()
    async def pause(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            song = await player.pause()
            await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command()
    async def resume(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            song = await player.resume()
            await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command()
    async def stop(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            await player.stop()
            await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command()
    async def loop(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            try:
                song = await player.toggle_song_loop()
            except DiscordUtils.NotPlaying:
                em=discord.Embed(description="There currently isn't a song playing", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command()
    async def queue(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            songs = player.current_queue()
            if songs != [] and len(songs) != 0:
                em=discord.Embed(title="Queue", description="\n".join(f"[{songs.index(song)+1}] `{song.name}`" for song in songs), color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"There aren't any songs in the queue", color=color())
                await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)
        try:
            song = player.now_playing()
            song.title
        except AttributeError:
            em=discord.Embed(description="There currently isn't a song playing", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(title=song.title, url=song.url, color=color())
            em.add_field(name="Channel", value=f"[{song.channel}]({song.channel_url})", inline=True)
            em.add_field(name="Duration", value=str(datetime.timedelta(seconds=song.duration)), inline=True)
            em.add_field(name="Looping", value="".join(self.bot.icons['greentick'] if song.is_looping == True else self.bot.icons['redtick']))
            em.set_footer(text=f"👁️ {humanize.intcomma(song.views)}")
            em.set_thumbnail(url=song.thumbnail)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    async def skip(self, ctx):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            data = await player.skip(force=True)
            await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, vol):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            player = self.music.get_player(guild_id=ctx.guild.id)
            try:
                await player.change_volume(float(vol) / 100)
            except AttributeError:
                em=discord.Embed(description="There currently isn't a song playing", color=color())
                await ctx.reply(embed=em, mention_author=False)
            else:
                await ctx.message.add_reaction(self.bot.icons["greentick"])

    @commands.command()
    async def remove(self, ctx, index : int):
        if not is_vc(ctx, ctx.author):
            await ctx.message.add_reaction(self.bot.icons["redtick"])
            em=discord.Embed(description=f"You are not in my voice channel", color=color())
            await ctx.reply(embed=em, mention_author=False)
        else:
            index = index - 1
            player = self.music.get_player(guild_id=ctx.guild.id)
            song = await player.remove_from_queue(index)
            await ctx.message.add_reaction(self.bot.icons["greentick"])

def setup(bot):
    bot.add_cog(Music(bot))
