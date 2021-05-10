# Import
import asyncio
import random
from itertools import cycle
import discord
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class CASINO(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    @Utils.Wrappers.TimeLogger
    def win_calculator(colour, aspect):
        rnum = random.randint(0, 36)
        rcolor = random.choice(["Rot", "Schwarz"])

        if aspect == "even" and (rnum % 2) == 0 and rcolor == colour:
            return True, rnum, rcolor

        elif aspect == "odd" and rcolor == colour and (rnum % 2) != 0:
            return True, rnum, rcolor

        else:

            return False, rnum, rcolor

    @commands.command(aliases=["rou"])
    @Utils.Wrappers.TimeLogger
    async def roulette(self, ctx, cred: int):

        # CHECK
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in valid_reactions

        valid_reactions = ['⚫', '🔴', '➖', '✖️']
        schwarz = "⚫"
        rot = "🔴"
        gerade = "➖"
        ungerade = "✖️"

        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        if data.lock is True:

            raise Utils.CreditError("Dein Konto wurde von einem Administrator gesperrt!")

        elif cred > int(data.bal):

            raise Utils.CreditError(
                "Du willst mehr Credits ausgeben als du hast!")

        else:

            embed = discord.Embed(
                title="Roulette",
                colour=discord.Colour(Utils.Farbe.Red),
                description="Wähle zwischen schwarz (⚫) / rot (🔴) und gerade (➖) / ungerade(✖️)"
            )

            await ctx.message.delete()
            m1 = await ctx.send(embed=embed)
            await m1.add_reaction("⚫")
            await m1.add_reaction("🔴")

            try:

                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            except asyncio.TimeoutError:

                erembed = discord.Embed(
                    title='Roulette',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{ctx.author.mention} hat nicht rechtzeitig reagiert.'
                )
                await m1.edit(embed=erembed)
                await asyncio.sleep(9)
                await m1.delete()
                return

            if str(reaction.emoji) == schwarz:

                reaktionf = "Schwarz"
                await m1.clear_reactions()


            elif str(reaction.emoji) == rot:

                reaktionf = "Rot"
                await m1.clear_reactions()

            await m1.add_reaction("➖")
            await m1.add_reaction("✖️")

            try:

                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            except asyncio.TimeoutError:

                erembed = discord.Embed(
                    title='Roulette',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{ctx.author.mention} hat nicht rechtzeitig reagiert.'
                )
                await m1.edit(embed=erembed)
                await asyncio.sleep(9)
                await m1.delete()
                return

            if str(reaction.emoji) == gerade:

                reaktionz = "even"
                await m1.clear_reactions()


            elif str(reaction.emoji) == ungerade:

                reaktionz = "odd"
                await m1.clear_reactions()

            await self.Roulette2(ctx, reaktionf, reaktionz, m1, cred)


    async def Roulette2(self, ctx, reaktionf, reaktionz, m1, cred: int):

        outcome, rnum, rcolor = CASINO.win_calculator(reaktionf, reaktionz)

        new_cred = int(cred) * 2

        if outcome is True:
            embed = discord.Embed(
                title="Roulette",
                colour=discord.Colour(Utils.Farbe.Lp_Green),
                description=f"Du hast gewonnen! Es war die Zahl {rnum} mit der Farbe {rcolor}!\nEs wurden **{new_cred}**₹ auf dein Konto überwiesen."
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)

            await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)

            await Utils.Messaging.Universal_edit(m1, embed, 15)

        else:

            embed = discord.Embed(
                title="Roulette",
                colour=discord.Colour(Utils.Farbe.Dp_Red),
                description=f"Du hast verloren! Es war die Zahl {rnum} mit der Farbe {rcolor}!\nEs wurden **{cred}**₹ von deinem Konto abgebucht."
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)

            await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)

            await Utils.Messaging.Universal_edit(m1, embed, 15)


    @commands.command(aliases=['bj'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @Utils.Wrappers.TimeLogger
    async def bj_game(self, ctx, cred: int):

        hit = '⬇'
        stand = '⏹'

        '❤️'
        '♦️'
        '♠️'
        '♣️'

        valid_reactions = ['⬇', '⏹']

        myDeck = Utils.BlackJack_Bot.Deck()
        hands = Utils.BlackJack_Bot.createPlayinghands(myDeck)
        dealer = hands[0]
        player = hands[1]

        Utils.BlackJack_Bot.pointCount(player)

        new_bal = cred * 2

        chars = ["'", ","]

        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        if data.lock is True:

            raise Utils.CreditError("Dein Konto wurde von einem Administrator gesperrt!")


        elif cred not in range(100, 20000) or cred > (int(data.bal) - 100):

            raise Utils.CreditError(
                "Du willst mehr Credits ausgeben als du hast / Mehr setzten als erlaubt ist / Weniger als die Mindestangabe verwenden! (Du musst mind. 100 Credits in der Bank lassen und nicht mehr als 20000 / weniger als 250 setzten.)")

        else:

            for p in chars:

                if Utils.BlackJack_Bot.pointCount(player) == 21:
                    embed = discord.Embed(
                        title='!!BLACKJACK!!',
                        colour=discord.Colour(Utils.Farbe.Lp_Green),
                        description=f'{ctx.author.mention}, du hast einen BLACKJACK!\n**Du hast somit Gewonnen!**\nDir wurden: **{new_bal}**₹ überwiesen!'
                    )
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**',
                                    value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(dealer))}')
                    embed.set_thumbnail(url=ctx.author.avatar_url)

                    await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)

                    await Utils.Messaging.Universal_send(ctx, embed, 10)

                    return

                elif Utils.BlackJack_Bot.pointCount(dealer) == 21:
                    embed = discord.Embed(
                        title='!!BLACKJACK!!',
                        colour=discord.Colour(Utils.Farbe.Dp_Red),
                        description=f'{ctx.author.mention}, der Dealer hat einen BLACKJACK!\n**Du hast somit Verloren!**\nDir wurden: **{cred}**₹ entzogen! '
                    )
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**',
                                    value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(dealer))}')

                    await Utils.Messaging.Universal_send(ctx, embed, 10)
                    await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                    return

                elif Utils.BlackJack_Bot.pointCount(player) > 21 and Utils.BlackJack_Bot.pointCount(dealer) > 21:
                    embed = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Darker_Theme),
                        description=f'{ctx.author.mention}, ihr habt beide mehr als 21!\n**Keiner hat Gewonnen!**\nDir wurden: **{cred}**₹ entzogen!'
                    )
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**',
                                    value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(dealer))}')
                    embed.set_thumbnail(url=self.client.user.avatar_url)

                    await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                    await Utils.Messaging.Universal_send(ctx, embed, 10)
                    return

                elif Utils.BlackJack_Bot.pointCount(player) > 21 > Utils.BlackJack_Bot.pointCount(dealer):
                    embed = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Dp_Red),
                        description=f'{ctx.author.mention}, du hast mehr als 21!\n**Du hast somit Verloren!**\nDir wurden: **{cred}**₹ entzogen!'
                    )
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**',
                                    value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(dealer))}')
                    embed.set_thumbnail(url=self.client.user.avatar_url)

                    await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                    await Utils.Messaging.Universal_send(ctx, embed, 10)
                    return

                elif Utils.BlackJack_Bot.pointCount(dealer) > 21 > Utils.BlackJack_Bot.pointCount(player):
                    embed = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Lp_Green),
                        description=f'{ctx.author.mention}, der Dealer hat mehr als 21!\n**Du hast somit Gewonnen!**\nDir wurden: **{new_bal}**₹ überwiesen!'
                    )
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**',
                                    value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(dealer))}')
                    embed.set_thumbnail(url=ctx.author.avatar_url)

                    await Utils.Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)
                    await Utils.Messaging.Universal_send(ctx, embed, 10)
                    return

                else:
                    embed = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f'{ctx.author.mention} um eine Karte zu ziehen tippe (⬇), um zu halten tippe (⏹).'
                    )
                    embed.add_field(name='**Deine Hand:**',
                                    value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Bot.pointCount(player))}')
                    embed.add_field(name='**Dealer Hand:**', value=f'{str(dealer[0]).replace(p, " ")}')

                    await ctx.message.delete()
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(2)
                    await m.add_reaction('⬇')
                    await m.add_reaction('⏹')

                    # CHECK
                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in valid_reactions

                    try:

                        reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)

                    except asyncio.TimeoutError:

                        erembed = discord.Embed(
                            title='Roulette',
                            colour=discord.Colour(Utils.Farbe.Red),
                            description=f'{ctx.author.mention} hat nicht rechtzeitig reagiert.'
                        )
                        await m.clear_reactions()
                        await m.edit(embed=erembed)
                        await asyncio.sleep(9)
                        await m.delete()
                        return

                    avatar = self.client.user.avatar_url

                    if str(reaction.emoji) == hit:
                        player.append(myDeck.pop())

                        if "Ass" in dealer:
                            pass
                        elif Utils.BlackJack_Bot.pointCount(dealer) < 15:
                            while Utils.BlackJack_Bot.pointCount(dealer) < 15:
                                if Utils.BlackJack_Bot.pointCount(dealer) < 15:
                                    dealer.append(myDeck.pop())
                                else:
                                    break

                        await Utils.BlackJack_Bot.win_evaluation_bot(self, ctx, dealer, player, m, avatar, cred)
                        return

                    elif str(reaction.emoji) == stand:

                        if "Ass" in dealer:
                            pass
                        elif Utils.BlackJack_Bot.pointCount(dealer) < 15:
                            while Utils.BlackJack_Bot.pointCount(dealer) < 15:
                                if Utils.BlackJack_Bot.pointCount(dealer) < 15:
                                    dealer.append(myDeck.pop())
                                else:
                                    break

                        await Utils.BlackJack_Bot.win_evaluation_bot(self, ctx, dealer, player, m, avatar, cred)
                        return

    @commands.command(aliases=["bjd"])
    @Utils.Wrappers.TimeLogger
    async def blackjack_d(self, ctx, user: discord.Member):

        myDeck = Utils.BlackJack_Duell.Deck()
        hands = Utils.BlackJack_Duell.createPlayinghands(myDeck)
        pl1P = hands[0]
        pl2P = hands[1]

        Utils.BlackJack_Duell.pointCount(pl1P)
        Utils.BlackJack_Duell.pointCount(pl2P)

        pl1 = ctx.author
        pl2 = user

        ei = "1️⃣"
        zw = "2️⃣"
        dr = "3️⃣"

        '❤️'
        '♦️'
        '♠️'
        '♣️'

        hit = "⬇"
        stand = "⏹"

        chars = ["'", ","]

        valid_reactions = ['1️⃣', '2️⃣', '3️⃣', '⬇', '⏹']

        auth = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)
        us = await Utils.Uccounts.check_Uccount(self, ctx, user.id, 1)

        if auth.lock or us.lock is True:

            raise Utils.CreditError("Eines angegebenen Konten wurde von einem Administrator gesperrt!")


        elif (int(auth.bal) - 100) < 1000:

            raise Utils.CreditError(
                f"{ctx.author.name}, du musst mind. 1000 Credits besitzen! (Du musst mind. 100 Credits in der Bank lassen.)")

        elif (int(us.bal) - 100) < 1000:

            raise Utils.CreditError(
                f"{user.name}, du musst mind. 1000 Credits besitzen! (Du musst mind. 100 Credits in der Bank lassen.)")


        else:

            await ctx.message.delete()

            embed = discord.Embed(
                title="-BLACK-JACK-",
                colour=discord.Colour(Utils.Farbe.Red),
                description=f"{ctx.author.mention}|{user.mention} bitte wählt euren Geldbetrag gemeinsam. **100**₹ (1️⃣), **500**₹ (2️⃣), **1000**₹ (3️⃣)\n**Der Command-Starter muss zuerst auswählen, die Auswahl kann nicht"
                            f" Rückgängig gemacht werden!**"
            )

            st = await ctx.send(embed=embed)
            await st.add_reaction("1️⃣")
            await st.add_reaction("2️⃣")
            await st.add_reaction("3️⃣")

            # CHECK
            def check1(reaction, user_n):
                return user_n == ctx.author and str(reaction.emoji) in valid_reactions

            def check2(reaction, user_n):
                return user_n == user and str(reaction.emoji) in valid_reactions

            try:
                reaction1, user1 = await self.client.wait_for('reaction_add', timeout=120.0, check=check1)

            except asyncio.TimeoutError:

                erembed = discord.Embed(
                    title='Roulette',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{ctx.author.mention} hat nicht rechtzeitig reagiert.'
                )
                await Utils.Messaging.Universal_edit(ctx, erembed, 15)
                return
            try:
                reaction2, user2 = await self.client.wait_for('reaction_add', timeout=120.0, check=check2)

            except asyncio.TimeoutError:

                erembed = discord.Embed(
                    title='Roulette',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{user.mention} hat nicht rechtzeitig reagiert.'
                )
                await Utils.Messaging.Universal_edit(ctx, erembed, 15)
                return

            if not str(reaction1.emoji) == str(reaction2.emoji):

                embed = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f"**Ihr habt nicht den selben Betrag gewählt!**"
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                return await Utils.Messaging.Universal_edit(st, embed, 15)

            else:

                if str(reaction1.emoji) and str(reaction2.emoji) == ei:
                    cred = 100

                elif str(reaction1.emoji) and str(reaction2.emoji) == zw:
                    cred = 500

                elif str(reaction1.emoji) and str(reaction2.emoji) == dr:
                    cred = 1000

                for p in chars:
                    embed = discord.Embed(
                        title="-BLACK-JACK-",
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f"{ctx.author.mention}|{user.mention} **schaut in eure Privatnachrichten!**"
                    )
                    embed.set_thumbnail(url=self.client.user.avatar_url)

                    await st.edit(embed=embed)

                    pl1E = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f'{pl1.name} um eine Karte zu ziehen tippe (⬇), um zu halten tippe (⏹).'
                    )
                    pl1E.add_field(name=f'**Deine Hand:**',
                                   value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Duell.pointCount(pl1P))}')
                    pl1E.add_field(name=f'**{pl2.name}`s Hand:**', value=f'{str(pl2P[0]).replace(p, " ")}')

                    pl2E = discord.Embed(
                        title="-BLACK-JACK-",
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f"{pl2.name}, bitte warte bis {pl1.name} seine Auswahl getroffen hat."
                    )

                    Embed_pl2 = await pl2.send(embed=pl2E)

                    Embed_pl1 = await pl1.send(embed=pl1E)

                    await asyncio.sleep(2)
                    await Embed_pl1.add_reaction("⬇")
                    await Embed_pl1.add_reaction("⏹")

                    try:
                        reaction1, user_new1 = await self.client.wait_for('reaction_add', timeout=60.0, check=check1)

                    except asyncio.TimeoutError:

                        erembed = discord.Embed(
                            title='-BLACK_JACK-',
                            colour=discord.Colour(Utils.Farbe.Red),
                            description=f'{pl1.name} hat nicht rechtzeitig reagiert.'
                        )

                        await Embed_pl1.edit(embed=erembed)
                        await Embed_pl2.edit(embed=erembed)
                        return

                    pl1E = discord.Embed(
                        title='-BLACK-JACK-',
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f'Bitte warte, bis {pl2.name} seine Auswahl getroffen hat.'
                    )

                    await Embed_pl1.edit(embed=pl1E)
                    await st.delete()

                    pl2E = discord.Embed(
                        title='-BLACKJACK-',
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f'{pl2.name} um eine Karte zu ziehen tippe (⬇), um zu halten tippe (⏹).'
                    )
                    pl2E.add_field(name=f'**Deine Hand:**',
                                   value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(Utils.BlackJack_Duell.pointCount(pl2P))}')
                    pl2E.add_field(name=f'**{pl1.name}`s Hand:**', value=f'{str(pl1P[1]).replace(p, " ")}')

                    await Embed_pl2.edit(embed=pl2E)

                    await asyncio.sleep(2)
                    await Embed_pl2.add_reaction('⬇')
                    await Embed_pl2.add_reaction('⏹')

                    try:
                        reaction2, user_new2 = await self.client.wait_for('reaction_add', timeout=60.0, check=check2)

                    except asyncio.TimeoutError:

                        erembed = discord.Embed(
                            title='-BLACKJACK-',
                            colour=discord.Colour(Utils.Farbe.Red),
                            description=f'{pl2.name} hat nicht rechtzeitig reagiert.'
                        )

                        await Embed_pl1.edit(embed=erembed)
                        await Embed_pl2.edit(embed=erembed)
                        return

                    if str(reaction1.emoji) == hit and str(reaction2.emoji) == hit:

                        pl1P.append(myDeck.pop())
                        pl2P.append(myDeck.pop())

                        await asyncio.sleep(1)

                        pl1Ev, pl2Ev = await Utils.BlackJack_Duell.win_evaluation(pl1, pl2, Embed_pl1, Embed_pl2, pl1P,
                                                                                  pl2P, cred)
                        if pl1Ev == 1:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "*", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "-", cred)
                        elif pl1Ev == 0:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "-", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "*", cred)

                        else:
                            pass

                        return

                    elif str(reaction1.emoji) == stand and str(reaction2.emoji) == stand:

                        await asyncio.sleep(1)

                        pl1Ev, pl2Ev = await Utils.BlackJack_Duell.win_evaluation(pl1, pl2, Embed_pl1, Embed_pl2,
                                                                                  pl1P, pl2P, cred)
                        if pl1Ev == 1:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "*", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "-", cred)
                        elif pl1Ev == 0:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "-", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "*", cred)
                        else:
                            pass

                        return

                    elif str(reaction1.emoji) == hit and str(reaction2.emoji) == stand:

                        pl1P.append(myDeck.pop())

                        await asyncio.sleep(1)

                        pl1Ev, pl2Ev = await Utils.BlackJack_Duell.win_evaluation(pl1, pl2, Embed_pl1, Embed_pl2,
                                                                                  pl1P, pl2P, cred)
                        if pl1Ev == 1:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "*", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "-", cred)
                        elif pl1Ev == 0:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "-", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "*", cred)
                        else:
                            pass

                        return

                    elif str(reaction1.emoji) == stand and str(reaction2.emoji) == hit:

                        pl2P.append(myDeck.pop())

                        await asyncio.sleep(1)

                        pl1Ev, pl2Ev = await Utils.BlackJack_Duell.win_evaluation(pl1, pl2, Embed_pl1, Embed_pl2,
                                                                                  pl1P, pl2P, cred)
                        if pl1Ev == 1:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "*", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "-", cred)
                        elif pl1Ev == 0:
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl1.id, "-", cred)
                            await Utils.Uccounts.currencyUp_Uccount(self, ctx, pl2.id, "*", cred)
                        else:
                            pass

                    return

    @commands.command()
    @Utils.Wrappers.TimeLogger
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, ctx):

        # Lokale Variablen

        Grape = "🍇"
        Cherry = "🍒"
        Orange = "🍊"
        Melon = "🍉"
        Lemon = "🍋"

        Wheel1 = random.choice(
            [f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}", f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}{Melon}{Lemon}"])

        Wheel2 = random.choice(
            [f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}", f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}{Melon}{Lemon}"])

        Wheel3 = random.choice(
            [f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}", f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}",
             f"{Grape}{Cherry}{Orange}{Melon}{Lemon}{Grape}{Cherry}{Orange}{Melon}{Lemon}"])

        Wheel1C = cycle(Wheel1)
        Wheel1Co = Wheel1

        Wheel2C = cycle(Wheel2)
        Wheel2Co = Wheel2

        Wheel3C = cycle(Wheel3)
        Wheel3Co = Wheel3

        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 1)

        if data.lock is True:
            raise Utils.CreditError("Dein Konto wurde von einem Administrator gesperrt!")

        elif data.bal <= 100:
            raise Utils.CreditError("Du musst mindestens 100 Credits auf dem Konto lassen!")

        else:

            embed = discord.Embed(
                title="-SLOT-MASCHINE-",
                colour=discord.Colour(Utils.Farbe.Red),
            )
            embed.add_field(name="1️⃣", value="**/**")
            embed.add_field(name="2️⃣", value="**/**")
            embed.add_field(name="3️⃣", value="**/**")

            await ctx.message.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(1)

            for _ in Wheel1Co:
                embed = discord.Embed(
                    title="-SLOT-MASCHINE-",
                    colour=discord.Colour(Utils.Farbe.Red),
                )
                embed.add_field(name="1️⃣", value=f"{next(Wheel1C)}")
                embed.add_field(name="2️⃣", value="**/**")
                embed.add_field(name="3️⃣", value="**/**")

                await m.edit(embed=embed)
                await asyncio.sleep(0.35)

            await asyncio.sleep(0.5)

            for _ in Wheel2Co:
                embed = discord.Embed(
                    title="-SLOT-MASCHINE-",
                    colour=discord.Colour(Utils.Farbe.Red),
                )
                embed.add_field(name="1️⃣", value=f"{Wheel1Co[-1:]}")
                embed.add_field(name="2️⃣", value=f"{next(Wheel2C)}")
                embed.add_field(name="3️⃣", value="**/**")

                await m.edit(embed=embed)
                await asyncio.sleep(0.35)

            await asyncio.sleep(0.5)

            for _ in Wheel3Co:
                embed = discord.Embed(
                    title="-SLOT-MASCHINE-",
                    colour=discord.Colour(Utils.Farbe.Red),
                )
                embed.add_field(name="1️⃣", value=f"{Wheel1Co[-1:]}")
                embed.add_field(name="2️⃣", value=f"{Wheel2Co[-1:]}")
                embed.add_field(name="3️⃣", value=f"{next(Wheel3C)}")

                await m.edit(embed=embed)
                await asyncio.sleep(0.35)

            await asyncio.sleep(1)

            new_embed = await Utils.Win_evaluation.SlotMachine.win_evaluation_slot(self, ctx, Wheel1Co[-1:], Wheel2Co[-1:], Wheel3Co[-1:], m)

            await Utils.Messaging.Universal_edit(m, new_embed, 15)


# Cog Finishing


def setup(client):
    client.add_cog(CASINO(client))
