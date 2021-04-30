# Import
import asyncio
import discord
from discord.ext import commands
from datetime import datetime

# Utils
import Utils


# Cog Initialising


class ADMINISTRATION(commands.Cog):
    def __init__(self, client):
        self.client = client

    # BAN

    @commands.command()
    @Utils.Permissions.Ban_perm()
    @Utils.Wrappers.TimeLogger
    async def ban(self, ctx, user: discord.Member, *, reason="Keinen Grund angegeben."):

        embed = discord.Embed(
            title=f'Es gibt einen Rebellenspion in unserer Mitte... {user.name}...',
            colour=discord.Colour(Utils.Farbe.Dp_Red)
        )
        embed.add_field(name='**Spieler:**', value=f'{user.mention}')
        embed.add_field(name='**Grund:**', value=f'{reason}')
        embed.add_field(name='**Von:**', value=f'{ctx.author.mention}')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.message.delete()
        m = await ctx.send(embed=embed)
        await user.send(embed=embed)
        await user.ban(reason=reason)
        await asyncio.sleep(15)
        await m.delete()

    # KICK

    @commands.command()
    @Utils.Permissions.Kick_perm()
    @Utils.Wrappers.TimeLogger
    async def kick(self, ctx, user: discord.Member, *, reason="Keinen Grund angegeben."):

        embed = discord.Embed(
            title=f"{user.name}, es geht mir nicht um Ehre, sondern Resultate für meinen Imperator.",
            colour=discord.Colour(Utils.Farbe.Dp_Red)
        )
        embed.add_field(name='**Spieler:**', value=f'{user.mention}')
        embed.add_field(name='**Grund:**', value=f'{reason}')
        embed.add_field(name='**Von:**', value=f'{ctx.author.mention}')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.message.delete()
        m = await ctx.send(embed=embed)
        await user.send(embed=embed)
        await user.kick(reason=reason)
        await asyncio.sleep(15)
        await m.delete()

    # CLEAR

    @commands.command(aliases=["c"])
    @Utils.Permissions.Clear_perm()
    @Utils.Wrappers.TimeLogger
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx, Anzahl):
        x = 0

        try:
            int(Anzahl)
            for _ in await ctx.channel.purge(limit=int(Anzahl)):
                x += 1

            embed = discord.Embed(
                title='Und so geht die Freiheit zu grunde - mit donnerndem Applaus',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'**{x}** Nachrichten gelöscht.\nWenn du alle Nachrichten löschen möchtest, gebe: `{self.client.command_prefix}c *` ein.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed)

        except:

            if Anzahl == '*':
                for _ in await ctx.channel.purge(limit=None):
                    x += 1

                embed = discord.Embed(
                    title='Und so geht die Freiheit zu grunde - mit donnerndem Applaus',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'**{x}** Nachrichten gelöscht.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed)

            else:
                raise commands.BadArgument(f"{Anzahl} ist nicht gültig, bitte gebe einen Integer(Zahl) oder * an.")

    # TELL

    @commands.command(aliases=["t"])
    @commands.has_permissions(administrator=True)
    @Utils.Wrappers.TimeLogger
    async def tell(self, ctx, *, Nachricht):

        embed = discord.Embed(
            title='',
            colour=discord.Colour(Utils.Farbe.Red),
            description=f'{Nachricht}'
        )

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def suptell(self, ctx, user: discord.Member, *, message):

        embed = discord.Embed(
            title="<SUPPORT>",
            colour=discord.Colour(Utils.Farbe.Red),
            description=f"{message}",
            timestamp=datetime.utcnow()
        )
        try:
            await ctx.message.delete()
        except:
            pass
        await user.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def masstell(self, ctx, *, message):

        embed = discord.Embed(
            title="<SUPPORT>",
            colour=discord.Colour(Utils.Farbe.Red),
            description=f"{message}",
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Massen-Benachrichtigung von Developer: {ctx.author.name}")


        try:
            await ctx.message.delete()
        except:
            pass

        for user in ctx.guild.members:
            try:
                await user.send(embed=embed)
            except:
                pass


# Cog Finishing


def setup(client):
    client.add_cog(ADMINISTRATION(client))
