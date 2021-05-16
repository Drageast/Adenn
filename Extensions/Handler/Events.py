# Import
import asyncio
import datetime
import random
import discord
from discord.ext import commands


# Framework
import Framework


# Cog Initialising


class EVENT(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.Uccount = Framework.Uccount(client)

    # MEMBER JOIN

    @commands.Cog.listener()
    async def on_member_join(self, user: discord.Member):

        embed = discord.Embed(
            title='**Willkommen!**',
            colour=Framework.Farbe.Red,
            description=f'{user.mention} willkommen auf dem Discord Server: **{user.guild.name}**'
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Mitgliederzahl:', value=f'{user.guild.member_count}')

        await Framework.get_channel(user, embed, 'willkommen')

    # MEMBER REMOVE

    @commands.Cog.listener()
    async def on_member_remove(self, user: discord.Member):

        embed = discord.Embed(
            title='**Bye!**',
            colour=Framework.Farbe.Dp_Red,
            description=f'Es war nett dich gekannt zu haben, {user.mention}!'
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Mitgliederzahl:', value=f'{user.guild.member_count}')

        await Framework.get_channel(user, embed, 'willkommen')

        self.Uccount.delete(user)

    # CLIENT JOIN

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        embed = discord.Embed(
            title='Hallo!',
            colour=discord.Colour(Framework.Farbe.Red),
            description='Hallo! Danke dass ihr mich hinzugefügt habt.\nDies sind die ersten Befehle, um anzufangen.'
        )
        embed.add_field(name='**!h**', value='Zeigt dir die Commands.')
        embed.add_field(name='**!s**', value='Support')
        embed.add_field(name='**Lege einen Kanal Namens _willkommen_ an**', value='Sendet dort Willkommensnachrichten.')
        embed.add_field(name='**Lege einen Kanal Namens _log_ an**',
                        value='Sendet wichtige Mitteilungen. (Nur für die Serveradministration)')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await guild.text_channels[0].send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.guild:
            return

        elif message.author.bot:
            return

        if message.content.startswith('!'):
            return

        elif message.content in [f'<@!{self.client.user.id}>', f'<@{self.client.user.id}>']:
            m = await message.channel.send(
                f'Hallo! Da du mich erwähnt hast, gehe ich davon aus, dass du meinen Präfix nicht mehr weißt.'
                f'Dieser ist: `{self.client.command_prefix}`')
            await asyncio.sleep(60)
            await m.delete()
            return

        else:

            data = self.Uccount.get(message.author, {"Get": {"Type": "CLASS", "Return": "LEVELING", "Timediff": True}})

            if data.Timestamp <= random.randint(-120, -1):

                self.Uccount.refactor(message.author, 5, ["Leveling", "Xp"], {"Type": "leveling", "Attributes": "+", "Timestamp": True})

                data.Xp += 5

                xp = data.Xp

                lvl = 0
                while True:
                    if xp < ((5 * (lvl ** 2)) + (5 * (lvl - 1))):
                        break
                    lvl += 1
                xp -= ((5 * ((lvl - 1) ** 2)) + (5 * (lvl - 1)))

                if xp == 0:
                    embed = discord.Embed(
                        title="Level Up!",
                        colour=Framework.Farbe.Red,
                        description=f"{message.author.mention} Glückwunsch! Du bist einen Level aufgestiegen! Du bist nun Level: **{lvl}**"
                    )
                    m = await message.channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await m.delete()

            else:
                pass


# Cog Finishing


def setup(client):
    client.add_cog(EVENT(client))
