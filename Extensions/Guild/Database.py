# Import
import discord
from discord.ext import commands
import asyncio

# Framework
import Framework


# Cog Initialising


class DB(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.Uccount = Framework.Uccount(client)
        self.Reactions = ["✅", "❎"]


    @commands.group(invoke_without_command=True, pass_context=True)
    async def db(self, ctx):
        await ctx.message.delete()

    @db.command()
    async def info(self, ctx):

        embed = discord.Embed(
            title="Information",
            colour=Framework.Farbe.Darker_Theme,
            description=f"Hallo und danke, dass du dich über meine Datenbank informieren möchtest!\nMeine Datenbank besteht aus [Python](https://www.python.org/) "
                        f"und [MongoDB](https://www.mongodb.com/) mit der Build-in-Library [Hashlib](https://docs.python.org/3/library/hashlib.html). "
                        f"\nEs werden keine Personen bezogene Daten gesammelt, was bedeutet, dass wir keinen Username oder sonstiges speichern, womit "
                        f"ein dritter dich in Verbindung bringt. Wir speichern nur deine Credits, Shimaris und Chat XP. Um dies zu bewerkstelligen, müssen wir dich allerdings "
                        f"über eine ID in der Datenbank identifizieren, aufgrund neuer Datenschutz Regeln von Discord, geschieht dies nun über den Hash Algorithmus [sha](https://de.wikipedia.org/wiki/Secure_Hash_Algorithm). "
                        f"Wir nehmen deine User ID, Hashen diese mit sha, damit keiner etwas damit anfangen kann und nutzen dies, um dich in der Datenbank zu identifizieren, worauf nur der Bot Zugriff hat."
        )

        await Framework.Messaging.Universal_send(ctx, embed, 120)

    @db.group()
    async def debug(self, ctx):
        await ctx.message.delete()

    @debug.command()
    @commands.is_owner()
    async def unset(self, ctx, user: discord.Member):

        self.Uccount.unset(user)
        await Framework.Messaging.Universal_send(ctx, f"`Guild Hash` von Nutzer `{user.name}` entfernt")

    @debug.command()
    @commands.is_owner()
    async def check(self, ctx, user: discord.Member):

        data = self.Uccount.get(user, {"Get": {"Type": "DICT", "Return": "ALL", "Timestamp": False}})

        data = f"Daten von: **{user.name}**```json\n{data}\n```"

        await Framework.Messaging.Universal_send(ctx, data, 35)



    @commands.command(aliases=["cred"])
    async def bal(self, ctx, user: discord.Member = None):
        User = ctx.author if user is None else user

        data = self.Uccount.get(User, {"Get": {"Type": "CLASS", "Return": "CURRENCY", "Timestamp": False}})

        embed = discord.Embed(
            title="",
            colour=Framework.Farbe.Lp_Blue,
        )
        embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Credits:", value=f"**{data.Balance}**₹")

        await Framework.Messaging.Universal_send(ctx, embed, 15)

    @commands.command()
    async def daily(self, ctx):
        data = self.Uccount.get(ctx.author, {"Get": {"Type": "CLASS", "Return": "CURRENCY", "Timestamp": True}})

        if data.Timestamp <= -43200:  # 12 Stunden

            self.Uccount.refactor(ctx.author, 2500, ["Currency", "Balance"], {"Type": "balance", "Attributes": "+", "Timestamp": True})

            embed = discord.Embed(
                title="",
                colour=Framework.Farbe.Lp_Blue,
                description=f"Du hast deine **2500**₹ eingesammelt, komme in 12 Stunden wieder!"
            )
            embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)

        else:
            embed = discord.Embed(
                title="",
                colour=Framework.Farbe.Red,
                description=f"Du musst noch warten, bis du deine Tägliche belohnung wieder einlösen kannst!"
            )
            embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)

    @commands.command(aliases=["trade"])
    async def transfer(self, ctx, user: discord.Member, Amount: int):

        # CHECK
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in self.Reactions

        author = self.Uccount.get(ctx.author, {"Get": {"Type": "CLASS", "Return": "CURRENCY", "Timestamp": False}})

        if author.Balance < Amount:
            embed = discord.Embed(
                title="",
                colour=Framework.Farbe.Red,
                description=f"Du besitzt nicht genug Geld, um es zu vergeben!"
            )
            embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

            return await Framework.Messaging.Universal_send(ctx, embed, 15)

        embed = discord.Embed(
            title="",
            colour=Framework.Farbe.Lp_Blue,
            description=f"Bist du sicher, dass du **{Amount}**₹  an _{user.name}_ übertragen möchtest?"
        )
        embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

        m1 = await ctx.send(embed=embed)

        await m1.add_reaction(self.Reactions[0])
        await m1.add_reaction(self.Reactions[1])

        try:

            reaction, user3 = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

        except asyncio.TimeoutError:

            erembed = discord.Embed(
                title="",
                colour=Framework.Farbe.Red,
                description=f"{ctx.author.name} hat nicht reagiert."
            )
            erembed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

            await Framework.Messaging.Universal_edit(m1, erembed, 15)
            return

        if str(reaction.emoji) == self.Reactions[1]:
            return await m1.delete()

        if str(reaction.emoji) == self.Reactions[0]:
            self.Uccount.refactor(ctx.author, Amount, ["Currency", "Balance"], {"Type": "balance", "Attributes": "-"})
            self.Uccount.refactor(user, Amount, ["Currency", "Balance"], {"Type": "balance", "Attributes": "+"})


            embed = discord.Embed(
                title="",
                colour=Framework.Farbe.Lp_Blue,
                description=f"**{Amount}**₹ wurden erfolgreich an _{user.mention}_ überwiesen."
            )
            embed.set_author(name="Credit Bank", icon_url=Framework.YAML.GET("Bilder", "Credits"))

            await Framework.Messaging.Universal_edit(m1, embed, 10)




# Cog Finishing


def setup(client):
    client.add_cog(DB(client))
