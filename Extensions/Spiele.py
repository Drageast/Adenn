# Import
import asyncio
import random
import discord
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ssp"])
    async def sspg(self, ctx):

        schere = '✌'
        stein = '✊'
        papier = '✋'

        valid_reactions = ['✌', '✊', '✋']

        embed = discord.Embed(
            title='Schere Stein Papier',
            colour=discord.Colour(Utils.Farbe.Red),
            description=f'{ctx.author.mention} \nWähle aus ob **Schere** (✌), **Stein** (✊) oder **Papier** (✋).'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        try:
            await ctx.message.delete()
        except:
            pass
        m = await ctx.send(embed=embed)
        await m.add_reaction(schere)
        await m.add_reaction(stein)
        await m.add_reaction(papier)

        # CHECK
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions

        try:

            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

        except asyncio.TimeoutError:

            erembed = discord.Embed(
                title='Schere Stein Papier',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'{ctx.author.mention} hat nicht rechtzeitig reagiert.'
            )
            return await Utils.Messaging.Universal_edit(m, erembed)

        rnum = random.randint(1, 3)

        if str(reaction.emoji) == schere:

            if rnum == 1:

                char = 'Schere'

                embed = discord.Embed(
                    title='Gleichstand!',
                    colour=discord.Colour(Utils.Farbe.Darker_Theme),
                    description=f'Ich hatte **{char}**.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            elif rnum == 2:

                char = 'Stein'

                embed = discord.Embed(
                    title='Verloren!',
                    colour=discord.Colour(Utils.Farbe.Dp_Red),
                    description=f'Ich hatte **{char}** und habe somit gewonnen.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            elif rnum == 3:

                char = 'Papier'

                embed = discord.Embed(
                    title='Gewonnen!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Ich hatte **{char}** und habe somit verloren.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)


        elif str(reaction.emoji) == stein:

            if rnum == 1:

                char = 'Schere'

                embed = discord.Embed(
                    title='Gewonnen!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Ich hatte **{char}** und habe somit verloren.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            elif rnum == 2:

                char = 'Stein'

                embed = discord.Embed(
                    title='Gleichstand!',
                    colour=discord.Colour(Utils.Farbe.Darker_Theme),
                    description=f'Ich hatte **{char}**.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            else:

                char = 'Papier'

                embed = discord.Embed(
                    title='Verloren!',
                    colour=discord.Colour(Utils.Farbe.Dp_Red),
                    description=f'Ich hatte **{char}** und habe somit gewonnen.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

        else:

            if rnum == 1:

                char = 'Schere'

                embed = discord.Embed(
                    title='Verloren!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Ich hatte **{char}** und habe somit gewonnen.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            elif rnum == 2:

                char = 'Stein'

                embed = discord.Embed(
                    title='Gewonnen!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Ich hatte **{char}** und habe somit verloren.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)

            else:

                char = 'Papier'

                embed = discord.Embed(
                    title='Gleichstand!',
                    colour=discord.Colour(Utils.Farbe.Darker_Theme),
                    description=f'Ich hatte **{char}**.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_edit(m, embed)


# Cog Finishing


def setup(client):
    client.add_cog(Games(client))
