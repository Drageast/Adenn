# Import
import discord
from discord.ext import commands, tasks
import random
import asyncio

# Utils
import Utils


# Cog Initialising


class ShimariCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.Numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        self.Failure = "🔴"
        State = Utils.YAML.GET("Variables", "ClientSide", "Status")
        if State == 1:
            self.interactive_Shimari.start()

    # Shimari Group

    @commands.group(invoke_without_command=True, pass_context=True)
    @Utils.Wrappers.TimeLogger
    async def Shi(self, ctx):
        embed = discord.Embed(
            title=":~Shimari~:",
            colour=discord.Colour(Utils.Farbe.ShimariRosa),
            description=f"Dies ist die Shimari Gruppe.\nDu kannst hier kämpfe starten und deinen Index ansehen.\n\n**[Shimari Info](https://github.com/Drageast/shimari-data)** -"
                        f" Daten können jeder Zeit geändert!"
        )
        await Utils.Messaging.Universal_send(ctx, embed, 15)

    # DEBUG Module

    @Shi.group(invoke_without_command=True, pass_context=True)
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def debug(self, ctx):
        embed = discord.Embed(
            title="DEBUG",
            colour=discord.Colour(Utils.Farbe.Red),
            description="Shimari Debug Bereich."
        )

        await Utils.Messaging.Universal_send(ctx, embed, 15)

    @debug.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def give(self, ctx, user: discord.Member, ID=None, Rarity=None):
        try:
            Shimari = (int(ID), int(Rarity))
        except:
            Shimari = Utils.Shimari.DiscordShimari.GET_randomShimari()

        await Utils.MongoDataBase.Uccounts.update_Shimari(self, ctx, user.id, Shimari, "+")

        m = f"**Du hast `{Shimari}` per Datenbank an `{user.name}` zugeordnet.**"

        await Utils.Messaging.Universal_send(ctx, m, 15)

    @debug.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def remove(self, ctx, user: discord.Member, ID, Seltenheit: int):
        Shimari_ = (ID, Seltenheit)

        try:
            await Utils.MongoDataBase.Uccounts.update_Shimari(self, ctx, user.id, Shimari_, "-")

            m = f"**Du hast `{Shimari_}` per Datenbank bei `{user.name}` entfernt.**"

        except Exception as e:

            m = f"Bei der Verarbeitung ist ein Fehler aufgetreten!\n`{e}`"

        await Utils.Messaging.Universal_send(ctx, m, 15)

    @debug.command()
    @commands.is_owner()
    @Utils.Wrappers.TimeLogger
    async def reboot(self, ctx):

        self.interactive_Shimari.restart()

        m = f"**Du hast `self.interactive_Shimari` neugestartet.**"

        await Utils.Messaging.Universal_send(ctx, m, 15)

    # Shimari Commands

    @Shi.command()
    @Utils.Wrappers.TimeLogger
    async def kampf(self, ctx, user: discord.Member):

        # CHECK
        def check1(reaction, user_):
            return user_ == ctx.author and str(reaction.emoji) in self.Numbers

        def check2(reaction, user_):
            return user_ == user and str(reaction.emoji) in self.Numbers

        list1 = await Utils.MongoDataBase.Uccounts.check_Uccount(self, ctx, ctx.author.id, 4)
        list2 = await Utils.MongoDataBase.Uccounts.check_Uccount(self, ctx, user.id, 4)

        embed = discord.Embed(
            title=f":~Shimari~:",
            colour=discord.Colour.dark_red(),
            description=f"{ctx.author.mention} bitte wähle ein Shimari zum Kämpfen:"
        )

        for index, Shimari in enumerate(list1.ShimariList):
            embed.add_field(name=f"{index + 1}", value=f"{Utils.Shimari.DiscordShimari.Create_Shimari(Shimari).Name}")

        m = await ctx.send(embed=embed)

        for i, _ in enumerate(list1.ShimariList):
            await m.add_reaction(self.Numbers[i])
        try:
            reaction, user_ = await self.client.wait_for("reaction_add", check=check1, timeout=60)
        except asyncio.TimeoutError:

            await m.edit(message=f"{ctx.author.mention} hat zu lange gewartet.")
            await asyncio.sleep(10)
            await m.delete()
            return

        index1 = 0 if str(reaction.emoji) == self.Numbers[0] else (
            1 if str(reaction.emoji) == self.Numbers[1] else (
                2 if str(reaction.emoji) == self.Numbers[2] else (
                    3 if str(reaction.emoji) == self.Numbers[3] else (
                        4 if str(reaction.emoji) == self.Numbers[4] else (
                            5 if str(reaction.emoji) == self.Numbers[5] else (
                                6 if str(reaction.emoji) == self.Numbers[6] else (
                                    7 if str(reaction.emoji) == self.Numbers[7] else (
                                        8 if str(reaction.emoji) == self.Numbers[8] else (
                                            9 if str(reaction.emoji) == self.Numbers[9] else ()
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        await m.clear_reactions()

        Author_Shimari = Utils.Shimari.DiscordShimari.Create_Shimari(list1.ShimariList[index1])

        embed = discord.Embed(
            title=f":~Shimari~:",
            colour=discord.Colour.dark_red(),
            description=f"{user.mention} bitte wähle ein Shimari zum Kämpfen:"
        )

        for index, Shimari in enumerate(list2.ShimariList):
            embed.add_field(name=f"{index + 1}", value=f"{Utils.Shimari.DiscordShimari.Create_Shimari(Shimari).Name}")

        await m.edit(embed=embed)

        for i, _ in enumerate(list2.ShimariList):
            await m.add_reaction(self.Numbers[i])
        try:
            reaction, user_ = await self.client.wait_for("reaction_add", check=check2, timeout=360)
        except asyncio.TimeoutError:

            await m.edit(message=f"{user.mention} hat zu lange gewartet.")
            await asyncio.sleep(10)
            await m.delete()
            return

        index2 = 0 if str(reaction.emoji) == self.Numbers[0] else (
            1 if str(reaction.emoji) == self.Numbers[1] else (
                2 if str(reaction.emoji) == self.Numbers[2] else (
                    3 if str(reaction.emoji) == self.Numbers[3] else (
                        4 if str(reaction.emoji) == self.Numbers[4] else (
                            5 if str(reaction.emoji) == self.Numbers[5] else (
                                6 if str(reaction.emoji) == self.Numbers[6] else (
                                    7 if str(reaction.emoji) == self.Numbers[7] else (
                                        8 if str(reaction.emoji) == self.Numbers[8] else (
                                            9 if str(reaction.emoji) == self.Numbers[9] else ()
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        await m.clear_reactions()

        User_Shimari = Utils.Shimari.DiscordShimari.Create_Shimari(list2.ShimariList[index2])

        while User_Shimari.Health >= 0 or Author_Shimari.Health >= 0 or User_Shimari.Energie >= 0 or Author_Shimari.Energie >= 0:

            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{user.mention} Wähle eine Attacke für: **{User_Shimari.Name}**!\n{User_Shimari.post_fight_data()}"
            )
            embed.set_image(url=User_Shimari.avatar())

            await m.edit(embed=embed)
            await m.add_reaction(self.Numbers[0])
            await m.add_reaction(self.Numbers[1])
            await m.add_reaction(self.Numbers[2])

            try:
                reaction, user_ = await self.client.wait_for("reaction_add", check=check2, timeout=60)
            except asyncio.TimeoutError:

                await m.edit(message=f"{user.mention} hat zu lange gewartet.")
                await asyncio.sleep(10)
                await m.delete()
                break

            attack1 = 1 if str(reaction.emoji) == self.Numbers[0] else (
                2 if str(reaction.emoji) == self.Numbers[1] else 3)

            data1 = Utils.Shimari.Shimari.fight(User_Shimari, Author_Shimari, attack1)

            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"Der Angriff von {user.mention} ist beendet!"
            )
            embed.add_field(name=f"Angreifer {user.name}/{User_Shimari.Name}:",
                            value=f"{User_Shimari.fight_data(data1.damage)}")
            embed.add_field(name=f"Verteidiger {ctx.author.name}/{Author_Shimari.Name}:",
                            value=f"{Author_Shimari.fight_data()}")

            await m.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(5)

            if User_Shimari.Health <= 0 or Author_Shimari.Health <= 0 or User_Shimari.Energie <= 0 or Author_Shimari.Energie <= 0:
                break

            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{ctx.author.mention} Wähle eine Attacke für: **{Author_Shimari.Name}**!\n{Author_Shimari.post_fight_data()}"
            )
            embed.set_image(url=Author_Shimari.avatar())

            await m.edit(embed=embed)
            await m.add_reaction(self.Numbers[0])
            await m.add_reaction(self.Numbers[1])
            await m.add_reaction(self.Numbers[2])

            try:
                reaction, user_ = await self.client.wait_for("reaction_add", check=check1, timeout=60)
            except asyncio.TimeoutError:

                await m.edit(message=f"{ctx.author.mention} hat zu lange gewartet.")
                await asyncio.sleep(10)
                await m.delete()
                break

            attack2 = 1 if str(reaction.emoji) == self.Numbers[0] else (
                2 if str(reaction.emoji) == self.Numbers[1] else 3)

            data2 = Utils.Shimari.Shimari.fight(Author_Shimari, User_Shimari, attack2)

            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"Der Angriff von {ctx.author.mention} ist beendet!"
            )
            embed.add_field(name=f"Angreifer {ctx.author.name}/{Author_Shimari.Name}:",
                            value=f"{Author_Shimari.fight_data(data2.damage)}")
            embed.add_field(name=f"Verteidiger {user.name}/{User_Shimari.Name}:", value=f"{User_Shimari.fight_data()}")

            await m.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(5)

            if User_Shimari.Health <= 0 or Author_Shimari.Health <= 0 or User_Shimari.Energie <= 0 or Author_Shimari.Energie <= 0:
                break

            Author_Shimari.random_Energie()
            User_Shimari.random_Energie()

        if User_Shimari.Health <= 0:
            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{ctx.author.mention} hat gewonnen!"
            )

            await Utils.Messaging.Universal_edit(m, embed, 15)
            return

        elif User_Shimari.Energie <= 0:
            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{ctx.author.mention} hat gewonnen!"
            )

            await Utils.Messaging.Universal_edit(m, embed, 15)
            return

        elif Author_Shimari.Health <= 0:
            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{user.mention} hat gewonnen!"
            )

            await Utils.Messaging.Universal_edit(m, embed, 15)
            return

        elif Author_Shimari.Energie <= 0:
            embed = discord.Embed(
                title=":~Shimari~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{user.mention} hat gewonnen!"
            )

            await Utils.Messaging.Universal_edit(m, embed, 15)
            return

        else:
            return

    @Shi.command()
    @Utils.Wrappers.TimeLogger
    async def dex(self, ctx, user: discord.Member = None):
        y = 0
        embeds = []

        User = ctx.author if user is None else user

        liste = await Utils.MongoDataBase.Uccounts.check_Uccount(self, ctx, User.id, 4.5)

        if not liste.ShimariList:
            y += 1
            embed = discord.Embed(
                title=f":~ShimarIdex : {User.name}~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"Dieser Nutzer besitzt noch keine Shimaris oder es ist ein Fehler aufgetreten."
            )
            embeds.append(embed)

        else:

            for index, Shimari in enumerate(liste.ShimariList):
                y += 1
                Shimari_ = Utils.Shimari.DiscordShimari.Create_Shimari(Shimari)

                embed = discord.Embed(
                    title=f":~Shimari Index[{index}] - Sammlung~:",
                    colour=discord.Colour(Utils.Farbe.ShimariRosa),
                    description=f"{Shimari_}"
                )
                embed.set_image(url=Shimari_.avatar())

                embeds.append(embed)

        inf = f"ShimarIdex von: **{User.name}** Seiten: `{y}`"

        await Utils.Messaging.Paginator(self, ctx, embeds, inf)

    @Shi.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sell(self, ctx):
        list1 = await Utils.MongoDataBase.Uccounts.check_Uccount(self, ctx, ctx.author.id, 4.5)
        embeds = []

        for index, obj in enumerate(list1.ShimariList):
            Shimari_ = Utils.Shimari.DiscordShimari.Create_Shimari(obj)
            embed = discord.Embed(
                title=":~Shop~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{Shimari_}"
            )
            embed.set_image(url=Shimari_.avatar())

            embeds.append(embed)

        await Utils.Shimari.DiscordShimari.ShimariShop(self, ctx, embeds, list1.ShimariList)

    @Shi.command()
    async def look(self, ctx, name=None, Debug=None):
        namee = None if name.lower() == "none" else (None if name is None else name)

        shimari_list = Utils.Shimari.DiscordShimari.list_control(namee)
        embeds = []

        for index, x in enumerate(shimari_list):
            embed = discord.Embed(
                title=f":~Shimari Index[{index}] - Liste~:",
                colour=discord.Colour(Utils.Farbe.ShimariRosa),
                description=f"{x}\n\n**Werte können abweichen!**"
            )
            embed.set_thumbnail(url=x.avatar())
            if Debug:
                if Debug.lower() == "key":
                    y = ""
                    for _, obj in enumerate(x.debug()):
                        y += f"{obj}\n"
                    embed.add_field(name="DEBUG:", value=f"`{y}`")

            embeds.append(embed)

        inf = f"Shimari Liste, bestehend aus dem gesuchtem Shimari" if name else f"Shimari Liste, bestehen aus allen Shimaris ({len(shimari_list)})"

        await Utils.Messaging.Paginator(self, ctx, embeds, inf)

    @tasks.loop(hours=2)
    @Utils.Wrappers.TimeLogger
    async def interactive_Shimari(self):
        await asyncio.sleep(10)
        y = 0
        guilds = []
        for guild in self.client.guilds:
            for user in guild.members:
                if user.bot:
                    pass
                elif str(user.status) != "offline":
                    y += 1

            if y >= 8:

                if random.randint(1, 10) <= 8:
                    guilds.append(guild)
                    y = 0

                else:
                    y = 0

            else:
                y = 0

        for guild in guilds:
            channel = discord.utils.get(guild.text_channels,
                                        name=Utils.YAML.GET("Variables", "ClientSide", "Channels", "Shimari"))

            def check(reaction, user):
                return str(reaction.emoji) == "❗" and user != user.bot

            while channel is not None:

                AI = Utils.Shimari.DiscordShimari.Create_Shimari(Utils.Shimari.DiscordShimari.GET_randomShimari())
                AI["Operator"] = "AI"

                embed = discord.Embed(
                    title=":~Shimari~:",
                    colour=discord.Colour(Utils.Farbe.ShimariRosa),
                    description=f"Ein Wildes Shimari ist aufgetaucht **({AI.Name})**! Der erste der die angegebene Reaktion anklickt, hat die chance dies zu fangen!"
                )
                embed.set_image(url=AI.avatar())

                m = await channel.send(embed=embed)

                await m.add_reaction("❗")
                await asyncio.sleep(1)
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60)
                except:
                    try:
                        await m.delete()
                    except:
                        break
                    break

                await m.delete()

                def check1(reaction, user_):
                    return str(reaction.emoji) in self.Numbers and user_ == user

                list = await Utils.MongoDataBase.Uccounts.check_Uccount(self, user, user.id, 4)

                embed = discord.Embed(
                    title=":~Shimari~:",
                    colour=discord.Colour(Utils.Farbe.ShimariRosa),
                    description=f"{user.mention} wähle dein Shimari für den Kampf!"
                )
                for index, Shimari in enumerate(list.ShimariList):
                    if index <= 9:
                        embed.add_field(name=f"{index + 1}",
                                        value=f"{Utils.Shimari.DiscordShimari.Create_Shimari(Shimari).Name}")
                    elif index == 10:
                        embed.add_field(name=f"-----",
                                        value=f"Ich kann max. die ersten 10 Shimaris anzeigen.")

                    else:
                        pass

                m = await channel.send(embed=embed)

                for i, _ in enumerate(list.ShimariList):
                    if i <= 9:
                        await m.add_reaction(self.Numbers[i])
                    else:
                        pass
                try:
                    reaction, _ = await self.client.wait_for("reaction_add", check=check1, timeout=60)
                except asyncio.TimeoutError:

                    await m.edit(message=f"{user.mention} hat zu lange gewartet.")
                    await asyncio.sleep(10)
                    await m.delete()
                    return

                index1 = 0 if str(reaction.emoji) == self.Numbers[0] else (
                    1 if str(reaction.emoji) == self.Numbers[1] else (
                        2 if str(reaction.emoji) == self.Numbers[2] else (
                            3 if str(reaction.emoji) == self.Numbers[3] else (
                                4 if str(reaction.emoji) == self.Numbers[4] else (
                                    5 if str(reaction.emoji) == self.Numbers[5] else (
                                        6 if str(reaction.emoji) == self.Numbers[6] else (
                                            7 if str(reaction.emoji) == self.Numbers[7] else (
                                                8 if str(reaction.emoji) == self.Numbers[8] else (
                                                    9 if str(reaction.emoji) == self.Numbers[9] else ()
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )

                await m.clear_reactions()

                User_Shimari = Utils.Shimari.DiscordShimari.Create_Shimari(list.ShimariList[index1])

                while User_Shimari.Health >= 0 or AI.Health >= 0 or User_Shimari.Energie >= 0 or AI.Energie >= 0:

                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"{user.mention} Wähle eine Attacke für: **{User_Shimari.Name}**!\n{User_Shimari.post_fight_data()}"
                    )
                    embed.set_image(url=User_Shimari.avatar())

                    await m.edit(embed=embed)
                    await m.add_reaction(self.Numbers[0])

                    button = Utils.Shimari.DiscordShimari.failure_chance()

                    if button == 1:
                        await m.add_reaction(self.Failure)
                        await m.add_reaction(self.Numbers[2])

                    elif button == 2:
                        await m.add_reaction(self.Numbers[1])
                        await m.add_reaction(self.Failure)

                    else:
                        await m.add_reaction(self.Numbers[1])
                        await m.add_reaction(self.Numbers[2])

                    try:
                        reaction, user_ = await self.client.wait_for("reaction_add", check=check1, timeout=60)
                    except asyncio.TimeoutError:

                        await m.edit(message=f"{user.mention} hat zu lange gewartet.")
                        await asyncio.sleep(10)
                        await m.delete()
                        break

                    attack1 = 1 if str(reaction.emoji) == self.Numbers[0] else (
                        2 if str(reaction.emoji) == self.Numbers[1] else 3)

                    data2 = Utils.Shimari.Shimari.fight(User_Shimari, AI, attack1)

                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"Der Angriff von {user.mention} ist beendet!"
                    )
                    embed.add_field(name=f"Angreifer {User_Shimari.Name}:",
                                    value=f"{User_Shimari.fight_data(data2.damage)}")
                    embed.add_field(name=f"Verteidiger {AI.Name}:", value=f"{AI.fight_data()}")

                    await m.delete()
                    m = await channel.send(embed=embed)
                    await asyncio.sleep(5)

                    if User_Shimari.Health <= 0 or AI.Health <= 0 or User_Shimari.Energie <= 0 or AI.Energie <= 0:
                        break

                    attack2 = Utils.Shimari.DiscordShimari.CALCULATE_Attack(AI)

                    data1 = Utils.Shimari.Shimari.fight(AI, User_Shimari, attack2)

                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"Der Angriff von **{AI.Name}** ist beendet!"
                    )
                    embed.add_field(name=f"Angreifer {AI.Name}:", value=f"{AI.fight_data(data1.damage)}")
                    embed.add_field(name=f"Verteidiger {User_Shimari.Name}:", value=f"{User_Shimari.fight_data()}")

                    await asyncio.sleep(1)
                    await m.delete()
                    m = await channel.send(embed=embed)
                    await asyncio.sleep(5)

                    if User_Shimari.Health <= 0 or AI.Health <= 0 or User_Shimari.Energie <= 0 or AI.Energie <= 0:
                        break

                    AI.random_Energie()
                    User_Shimari.random_Energie()

                if User_Shimari.Health <= 0:
                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"**{AI.Name}** hat gewonnen!"
                    )

                    await Utils.Messaging.Universal_edit(m, embed, 15)
                    return

                elif User_Shimari.Energie <= 0:
                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"**{AI.Name}** hat gewonnen!"
                    )

                    await Utils.Messaging.Universal_edit(m, embed, 15)
                    return

                elif AI.Health <= 0:
                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"{user.mention} hat gewonnen!\nDu hast das Shimari \n{Utils.Shimari.DiscordShimari.Create_Shimari(AI.tuple_Shimari())}\ngefangen!"
                    )
                    embed.set_image(url=AI.avatar())

                    await Utils.Uccounts.update_Shimari(self, user, user.id, AI.tuple_Shimari(), "+")
                    await Utils.Messaging.Universal_edit(m, embed, 15)
                    return

                elif AI.Energie <= 0:
                    embed = discord.Embed(
                        title=":~Shimari~:",
                        colour=discord.Colour(Utils.Farbe.ShimariRosa),
                        description=f"{user.mention} hat gewonnen!\nDu hast das Shimari \n{Utils.Shimari.DiscordShimari.Create_Shimari(AI.tuple_Shimari())}\ngefangen!"
                    )
                    embed.set_image(url=AI.avatar())

                    await Utils.Uccounts.update_Shimari(self, user, user.id, AI.tuple_Shimari(), "+")
                    await Utils.Messaging.Universal_edit(m, embed, 15)
                    return

                else:
                    return


# Cog Finishing


def setup(client):
    client.add_cog(ShimariCommands(client))
