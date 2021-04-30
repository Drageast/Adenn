# Import
import DiscordUtils
import discord
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class MUSIK(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.music = DiscordUtils.Music()


    @Utils.Wrappers.TimeLogger
    async def start_playing(self, ctx, url):
        try:
            try:
                if ctx.voice_client.is_playing():

                    player = self.music.get_player(guild_id=ctx.guild.id)
                    if not player:
                        player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)

                    async with ctx.typing():
                        song = await player.queue(url, search=True)


                    embed = discord.Embed(
                        title='',
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f'[{Utils.safe_format(song.name)}]({song.url})'
                    )
                    embed.set_author(name='Zur Playlist hinzugefügt:')
                    embed.set_image(url=song.thumbnail)
                    embed.set_footer(text=f'Hinzugefügt von: {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=self.client.user.avatar_url)

                    await Utils.Messaging.Universal_send(ctx, embed, 60)
                    return False

                else:
                    return True
            except:
                await ctx.voice_client.disconnect()
                await self.start_playing(ctx, url)
        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def play(self, ctx, *, url):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            if not player:
                player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
            if not ctx.voice_client.is_playing():
                await player.queue(url, search=True)
                song = await player.play()
                embed = discord.Embed(
                    title='',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'[{Utils.safe_format(song.name)}]({song.url})'
                )
                embed.set_author(name='Spielt gerade:')
                embed.set_image(url=song.thumbnail)
                embed.set_footer(text=f'Hinzugefügt von: {ctx.author.name}', icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)
            else:
                song = await player.queue(url, search=True)
                embed = discord.Embed(
                    title='',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'[{Utils.safe_format(song.name)}]({song.url})'
                )
                embed.set_author(name='Zur Playlist hinzugefügt:')
                embed.set_image(url=song.thumbnail)
                embed.set_footer(text=f'Hinzugefügt von: {ctx.author.name}', icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)

            try:
                while ctx.voice_client.is_connected():
                    if len(ctx.voice_client.channel.members) == 1:
                        await ctx.voice_client.disconnect()
                        break
                    elif ctx.voice_client.is_paused():
                        pass
                    elif ctx.voice_client.is_playing():
                        pass
                    else:
                        await ctx.voice_client.disconnect()
                        break
            except:
                try:
                    await ctx.voice_client.disconnect()
                except:
                    pass
                return
        except Exception as e:
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def stop(self, ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            await player.stop()
            await ctx.message.delete()

        except:
            raise Utils.MusicError(lambda error: error)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def resume(self, ctx):
        try:
            if ctx.voice_client.is_paused():
                player = self.music.get_player(guild_id=ctx.guild.id)
                await player.resume()
                await ctx.message.delete()
            else:

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description='Die Musik ist nicht pausiert!'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed)

        except Exception as e:

            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def pause(self, ctx):
        try:
            if ctx.voice_client.is_playing():
                player = self.music.get_player(guild_id=ctx.guild.id)
                await player.pause()
                await ctx.message.delete()

            else:

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description='Die Musik ist schon pausiert!'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.message.delete()

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def skip(self, ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            data = await player.skip(force=True)

            embed = discord.Embed(
                title='',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'[{Utils.safe_format(data[1].name)}]({data[1].url})'
            )
            embed.set_author(name='Übersprungen:')
            embed.set_image(url=data[1].thumbnail)
            embed.set_footer(text=f'Übersprungen von: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command(aliases=["v"])
    @Utils.Wrappers.TimeLogger
    async def volume(self, ctx, vol: float):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            song, volume = await player.change_volume(float(vol / 100))

            embed = discord.Embed(
                title='Lautstärke',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Lautstärke für **{Utils.safe_format(song.name)}** auf **{(volume * 100)}**% gestellt.'
            )
            embed.set_footer(text=f"Angepasst von: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            return await Utils.Messaging.Universal_send(ctx, embed, 15)

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def queue(self, ctx):

        x = 1

        try:
            player = self.music.get_player(guild_id=ctx.guild.id)

            embed = discord.Embed(
                title='',
                colour=discord.Colour(Utils.Farbe.Red)
            )
            embed.set_author(name='Playlist:')
            embed.set_thumbnail(url=self.client.user.avatar_url)

            for song in player.current_queue():
                embed.add_field(name=f"-<{x}>-", value=f"{song.name}")
                x += 1

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def remove(self, ctx, index: int):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            song = await player.remove_from_queue(int(index))

            embed = discord.Embed(
                title='',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f"**{song.name}** von der Playlist entfernt"
            )
            embed.set_author(name='Playlist:')
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        except Exception as e:
            raise Utils.MusicError(e)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def loop(self, ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            song = await player.toggle_song_loop()
            if song.is_looping:
                await Utils.Messaging.Universal_send(ctx, f"Loop für den Song: **{song.name}** aktiv.")
            else:
                await Utils.Messaging.Universal_send(ctx, f"Loop für den Song: **{song.name}** inaktiv.")

        except Exception as e:
            raise Utils.MusicError(e)



    @remove.before_invoke
    @loop.before_invoke
    @leave.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    @play.before_invoke
    @Utils.Wrappers.TimeLogger
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except Exception as e:
                    raise Utils.MusicError(e)
        else:
            pass


# Cog Finishing


def setup(client):
    client.add_cog(MUSIK(client))
