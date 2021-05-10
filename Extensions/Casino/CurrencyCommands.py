# Import
import asyncio
import datetime
import discord
from discord.ext import commands


# Utils
import Utils


# Cog Initialising


class CurCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.Reactions = ["✅", "❎"]


    @commands.command(aliases=["cred", "bal"])
    @Utils.Wrappers.TimeLogger
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        data = await Utils.MongoDataBase.Uccounts.check_Uccount(self, ctx, user.id, 1)
        colour = Utils.Farbe.Dp_Red if data.lock is True else Utils.Farbe.Red

        embed = discord.Embed(
            title="",
            colour=discord.Colour(colour),
        )
        embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Credits:", value=f"**{data.bal}**₹")
        embed.add_field(name="Sperrung:", value=f"{'Ja' if data.lock is True else 'Nein'}")

        await Utils.Messaging.Universal_send(ctx, embed, 15)


    @commands.command()
    @Utils.Wrappers.TimeLogger
    async def trade(self, ctx, cred: int, user: discord.Member):

        # CHECK
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in self.Reactions

        data_author = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        if data_author.lock is True:

            raise Utils.CreditError("Dein Konto wurde von einem Administrator gesperrt!")


        elif int(data_author.bal) < int(cred + 100):

            raise Utils.CreditError(
                "Du willst mehr Credits übertragen, als du besitzt! (Du musst mind. 100 Credits mehr haben, als du weggeben möchtest.)")


        else:

            embed = discord.Embed(
                title="",
                colour=discord.Colour(Utils.Farbe.Red),
                description=f"Bist du sicher, dass du **{cred}**₹ übertragen möchtest?"
            )
            embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))

            m1 = await ctx.send(embed=embed)

            await m1.add_reaction(self.Reactions[0])
            await m1.add_reaction(self.Reactions[1])

            try:

                reaction, user3 = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            except asyncio.TimeoutError:

                erembed = discord.Embed(
                    title="",
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f"{ctx.author.name} hat nicht reagiert."
                )
                erembed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))

                await m1.edit(embed=erembed)
                await asyncio.sleep(9)
                await m1.delete()
                return

            if str(reaction.emoji) == self.Reactions[1]:
                return await m1.delete()

            if str(reaction.emoji) == self.Reactions[0]:
                await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                await asyncio.sleep(1)

                await Utils.Uccounts.currencyUp_Uccount(self, ctx, user.id, "+", cred)

                author_data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)
                user_data = await Utils.Uccounts.check_Uccount(self, ctx, user.id, 1)

                embed = discord.Embed(
                    title="",
                    colour=discord.Colour(Utils.Farbe.Red),
                )
                embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))
                embed.add_field(name=f"{ctx.author.name} Credits:", value=f"**{author_data.bal}**₹")
                embed.add_field(name=f"{user.name} Credits:", value=f"**{user_data.bal}**₹")

                await Utils.Messaging.Universal_edit(m1, embed, 10)


    # Überarbeiten
    @commands.command(aliases=["dr"])
    @Utils.Wrappers.TimeLogger
    async def daily_reward(self, ctx):

        epoch = datetime.datetime.utcfromtimestamp(0)

        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        if data.diff > 12000:

            await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "+", 1000)

            await Utils.Uccounts.update_Uccount(self, ctx, ctx.author.id, "Casino", "Timestamp",
                                                (datetime.datetime.utcnow() - epoch).total_seconds())

            data2 = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

            embed = discord.Embed(
                title="",
                colour=discord.Colour(Utils.Farbe.Red),
            )
            embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))
            embed.add_field(name=f"{ctx.author.name} Credits:", value=f"**{data2.bal}**₹")

            await Utils.Messaging.Universal_send(ctx, embed, 10)


        else:

            raise Utils.CreditError("Du musst mind. 12 Stunden warten!")


    @commands.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def loce(self, ctx, user: discord.Member):
        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        choicec = Utils.Farbe.Lp_Green if data.lock is True else Utils.Farbe.Dp_Red
        choicet = f"Das Bank-Konto des Nutzers: {user.name} wurde entsperrt!" if data.lock is True else f"Das Bank-Konto des Nutzers: {user.name} wurde gesperrt!"
        choiceb = False if data.lock is True else True

        embed = discord.Embed(
            title="",
            colour=discord.Colour(choicec),
            description=f"{choicet}"
        )
        embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))

        await Utils.Uccounts.update_Uccount(self, ctx, ctx.author.id, "Casino", "Lock", choiceb)
        await Utils.Messaging.Universal_send(ctx, embed, 10)


# Cog Finishing


def setup(client):
    client.add_cog(CurCommands(client))
