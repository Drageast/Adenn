# Import
import asyncio
import random
import discord
from discord.ext import commands


# Utils
import Utils


# Cog Initialising


class SUPPORT(commands.Cog):

    def __init__(self, client):
        self.client = client

    # CHECKS

    async def wait_message(self, ctx):
        new_message = await self.client.wait_for('message', check=lambda message: message.author == ctx.author,
                                                 timeout=360.0)
        return new_message

    # ----

    # SUPPORT_ANFRAGE

    @commands.command(aliases=["s"])
    async def support(self, ctx):

        Ticket = random.randint(1000, 9999)

        # ANKÜNDIGUNG
        embed = discord.Embed(
            title='>**Support**<',
            colour=discord.Colour(Utils.Farbe.Red),
            description=f'{ctx.author.mention}, schaue in deine **Privaten** Nachrichten.'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.Messaging.Universal_send(ctx, embed, 4)

        # PRIVAT START
        embed = discord.Embed(
            title='>**Support**<',
            colour=discord.Colour(Utils.Farbe.Red),
            description='Hallo! Ich bin hier, um dir bei deinem Problem zu helfen.'
                        '\nBevor du mir dein Problem schilderst, gebe erstmal eine Stufe der Wichtigkeit an.'
                        '\n`1`: Vorschläge,'
                        '\n`2`: Kleine Fehler (bps. Rechtschreibfehler),'
                        '\n`3`: Mittlere Fehler (bsp. Aktionen werden nicht richtig ausgeführt),'
                        '\n`4`: Korrumpierung des Commands.'
                        '\n\nGibst du nichts ein, wird der Vorgang abgebrochen.'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        s1 = await ctx.author.send(embed=embed)

        try:

            m1 = await self.wait_message(ctx)

        except asyncio.TimeoutError:

            return

        if "1" in m1.content:
            Stufe = "1 -- Vorschlag"

        elif "2" in m1.content:
            Stufe = "2 -- Geringfügiger Fehler"

        elif "3" in m1.content:
            Stufe = "3 -- Mäßiger Fehler"

        elif "4" in m1.content:
            Stufe = "4 -- Korrumpierung"

        else:
            return

        embed = discord.Embed(
            title='>**Support**<',
            colour=discord.Colour(Utils.Farbe.Red),
            description=f'Danke für deine Angabe. Dein Ticket wird unter dem Label:\n`{Stufe}`\nversendet.'
                        '\nGebe bitte nun den Fehlerbericht ein, dieser sollte mind. 25 Zeichen enthalten.'
                        '\nWenn du jedoch den Vorgang abbrechen möchtest, gebe nichts ein.'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await s1.delete()
        s2 = await ctx.author.send(embed=embed)

        try:

            m2 = await self.wait_message(ctx)

        except asyncio.TimeoutError:

            return

        if len(m2.content) < 25:
            return

        else:
            embed = discord.Embed(
                title='>**Support**<',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Danke für deine Angabe.'
                            f'\nDu wirst demnächst eine Nachricht des Development-Teams erhalten.\n'
                            f'Dein Ticket:```{Ticket}```'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await s2.delete()
            await ctx.author.send(embed=embed)

            # MONGO_DB

            data2 = {
                "_id": f"{Ticket}",
                "Author": ctx.author.id,
                "Stufe": Stufe,
                "Message": m2.content}

            self.client.ticket.insert_one(data2)

            embed = discord.Embed(
                title=f'Support Anfrage von: **{ctx.author}**',
                colour=discord.Colour(Utils.Farbe.Dp_Green),
                description=f'```fix\nStufe: {Stufe}\n```\n```\nNachricht: {m2.content}\n```'
            )
            embed.add_field(name='**Antworten:**', value=f'`{self.client.command_prefix}a Ticket Nachricht`')
            embed.add_field(name='**TICKET:**', value=f'`{Ticket}`')

            user1 = await self.client.fetch_user(Utils.YAML.GET("Variables", "Developer")[0])
            user2 = await self.client.fetch_user(Utils.YAML.GET("Variables", "Developer")[1])

            await user1.send(embed=embed)
            await user2.send(embed=embed)

    # ANTWORTEN

    @commands.command(aliases=["a"])
    @commands.is_owner()
    @commands.dm_only()
    async def antwort(self, ctx, Ticket, *, n):

        User2 = await self.client.fetch_user(Utils.YAML.GET("Variables", "Developer")[0])
        User3 = await self.client.fetch_user(Utils.YAML.GET("Variables", "Developer")[1])

        _Ticket = self.client.ticket.find_one({"_id": Ticket})

        if _Ticket is None:
            return await ctx.send("**Dieses Ticket existiert nicht!**")

        else:

            if ctx.author == User2:
                embed = discord.Embed(
                    title=f'{User2.name} hat das Ticket: `{Ticket}` bearbeitet!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Antwort:```fix\n{n}\n```'
                )
                await User3.send(embed=embed)

            elif ctx.author == User3:
                embed = discord.Embed(
                    title=f'{User3.name} hat das Ticket: `{Ticket}` bearbeitet!',
                    colour=discord.Colour(Utils.Farbe.Lp_Green),
                    description=f'Antwort:```fix\n{n}\n```'
                )
                await User2.send(embed=embed)

            else:
                pass

            author_id = _Ticket["Author"]
            Nachricht = _Ticket["Message"]
            Stufe = _Ticket["Stufe"]
            user = await self.client.fetch_user(f'{author_id}')

            embed = discord.Embed(
                title='>**Support**<',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du hast eine Antwort des **Support Teams** erhalten!\n```\n- Dein Ticket: {Ticket}, {Stufe}, {Nachricht}\n```'
                            f'```diff\n- Antwort: {n}```'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await user.send(embed=embed)

            embed = discord.Embed(
                title=f'Du hast eine Antwort versendet!',
                colour=discord.Colour(Utils.Farbe.Dp_Green),
                description=f'Antwort:```fix\n{n}\n```'
            )
            await ctx.author.send(embed=embed)

            self.client.ticket.delete_one({"_id": Ticket})


# Cog Finishing


def setup(client):
    client.add_cog(SUPPORT(client))
