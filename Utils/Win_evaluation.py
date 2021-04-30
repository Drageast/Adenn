# Import
import random
from random import shuffle
import discord
from .MongoDataBase import Uccounts

# Util
from .Utilities import Farbe, Messaging, Wrappers


# Lokale_Variablen
hit = '⬇'
stand = '⏹'

herz = '❤️'
karo = '♦️'
pik = '♠️'
kreuz = '♣️'

valid_reactions = ['⬇', '⏹']

chars = ["'", ","]


class BlackJack_Duell:

    @staticmethod
    @Wrappers.TimeLogger
    def Deck():
        deck = []
        for suit in (random.choice([herz, karo, pik, kreuz])):
            for rank in ['Ass', '2', '3', '4', '5', '6', '7', '8', '9', 'Bube', 'Dame', 'König']:
                deck.append(suit + rank)

            shuffle(deck)
            return deck

    @staticmethod
    @Wrappers.TimeLogger
    def pointCount(myCards):
        myCount = 0
        aceCount = 0

        for i in myCards:
            if i[1] == 'B' or i[1] == 'D' or i[1] == 'K':
                myCount += 10

            elif i[1] != 'A':
                myCount += int(i[1])

            else:
                aceCount += 1

        if aceCount == 1 and myCount >= 10:
            myCount += 11

        elif aceCount != 0:
            myCount += 1

        return myCount

    @staticmethod
    @Wrappers.TimeLogger
    def createPlayinghands(myDeck):
        player1Hand = []
        player2Hand = []

        player1Hand.append(myDeck.pop())
        player1Hand.append(myDeck.pop())

        player2Hand.append(myDeck.pop())
        player2Hand.append(myDeck.pop())

        return [player1Hand, player2Hand]

    @staticmethod
    @Wrappers.TimeLogger
    async def win_evaluation(pl1, pl2, Embed_pl1, Embed_pl2, pl1P, pl2P, cred: int):

        for p in chars:

            if BlackJack_Duell.pointCount(pl1P) == 21:

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"Du hast einen Blackjack!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl2.name} wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"{pl1.name} hat einen Blackjack!\n{pl1.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 1, 0

            elif BlackJack_Duell.pointCount(pl2P) == 21:

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"Du hast einen Blackjack!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl1.name} wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"{pl2.name} hat einen Blackjack!\n{pl2.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 0, 1

            elif BlackJack_Duell.pointCount(pl2P) > 21 and BlackJack_Duell.pointCount(pl1P) > 21:
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{pl1.name} und {pl2.name} ihr habt beide über 21.\n**Ihr habt somit verloren!**\nEuch wurden **{cred}**₹ entzogen!'
                )
                embed.add_field(name=f'**{pl1.name}`s Hand:**',
                                value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                embed.add_field(name=f'**{pl2.name}`s Hand:**',
                                value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                await Embed_pl1.edit(embed=embed)
                await Embed_pl2.edit(embed=embed)
                return 0, 0

            elif BlackJack_Duell.pointCount(pl2P) > 21 > BlackJack_Duell.pointCount(pl1P):

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"{pl2.name} hat mehr als 21!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl2.name} wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"Du hast mehr als 21!\n{pl1.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 1, 0

            elif BlackJack_Duell.pointCount(pl1P) > 21 > BlackJack_Duell.pointCount(pl2P):

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"{pl1.name} hat mehr als 21!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl1.name} wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"Du hast mehr als 21!\n{pl2.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 0, 1


            elif BlackJack_Duell.pointCount(pl2P) > BlackJack_Duell.pointCount(pl1P):

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"Du hast mehr als {pl1.name}!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl1.name} wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"Du hast weniger als {pl2.name}!\n{pl2.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 0, 1

            elif BlackJack_Duell.pointCount(pl1P) > BlackJack_Duell.pointCount(pl2P):

                pl1E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f"Du hast mehr als {pl2.name}!\nDir wurden **{int(cred) * 2}**₹ überwiesen und {pl2.name} wurden **{cred}**₹ entzogen!"
                )
                pl1E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')
                pl1E.add_field(name=f'**{pl2.name}`s Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')

                pl2E = discord.Embed(
                    title="-BLACK-JACK-",
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f"Du hast weniger als {pl1.name}!\n{pl1.name} wurden **{int(cred) * 2}**₹ überwiesen und dir wurden **{cred}**₹ entzogen!"
                )
                pl2E.add_field(name=f'**Deine Hand:**',
                               value=f'{str(pl2P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl2P))}')
                pl2E.add_field(name=f'**{pl1.name}`s Hand:**',
                               value=f'{str(pl1P).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(pl1P))}')

                await Embed_pl1.edit(embed=pl1E)
                await Embed_pl2.edit(embed=pl2E)
                return 1, 0

            else:

                embed = discord.Embed(
                    title='Fehler!',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description='Ein Fehler in der Funktion: `wind_evaluation` ist aufgetreten!'
                )

                await Embed_pl1.edit(embed=embed)
                await Embed_pl1.edit(embed=embed)
                return 2, 2

    @staticmethod
    @Wrappers.TimeLogger
    async def win_condition(player1, player2, player1_E, player2_E, name_player1, name_player2):
        for p in chars:

            if BlackJack_Duell.pointCount(player2) == 21:
                embed = discord.Embed(
                    title='!!BLACKJACK!!',
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f'{name_player2} hat einen BLACKJACK!\n**{name_player2} hat somit Gewonnen!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player1) == 21:
                embed = discord.Embed(
                    title='!!BLACKJACK!!',
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f'{name_player1} hat einen BLACKJACK!\n**{name_player1} hat somit Gewonnen!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player2) > 21 and BlackJack_Duell.pointCount(player1) > 21:
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{name_player1} und {name_player2} ihr habt beide über 21.\n**Ihr habt somit verloren!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player2) > 21 > BlackJack_Duell.pointCount(player1):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{name_player2} hat mehr als 21!\n**{name_player2}hat somit Verloren!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player1) > 21 > BlackJack_Duell.pointCount(player2):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{name_player1} hat mehr als 21!\n**{name_player1}hat somit Verloren!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player2) > BlackJack_Duell.pointCount(player1):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{name_player2} hat mehr als {name_player1}.\n**{name_player2} hat somit gewonnen!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            elif BlackJack_Duell.pointCount(player1) > BlackJack_Duell.pointCount(player2):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'{name_player1} hat mehr als {name_player2}.\n**{name_player1} hat somit gewonnen!**'
                )
                embed.add_field(name=f'**{name_player1} Hand:**',
                                value=f'{str(player1).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player1))}')
                embed.add_field(name=f'**{name_player2} Hand:**',
                                value=f'{str(player2).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Duell.pointCount(player2))}')

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return

            else:

                embed = discord.Embed(
                    title='Fehler!',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description='Ein Fehler bei: **win_condition** ist aufgetreten'
                )

                await player1_E.edit(embed=embed)
                await player2_E.edit(embed=embed)
                return


# noinspection PyTypeChecker
class BlackJack_Bot:

    @staticmethod
    @Wrappers.TimeLogger
    def Deck():
        deck = []
        for suit in (random.choice([herz, karo, pik, kreuz])):
            for rank in ['Ass', '2', '3', '4', '5', '6', '7', '8', '9', 'Bube', 'Dame', 'König']:
                deck.append(suit + rank)

            shuffle(deck)
            return deck

    @staticmethod
    @Wrappers.TimeLogger
    def pointCount(myCards):
        myCount = 0
        aceCount = 0

        for i in myCards:
            if i[1] == 'B' or i[1] == 'D' or i[1] == 'K':
                myCount += 10

            elif i[1] != 'A':
                myCount += int(i[1])

            else:
                aceCount += 1

        if aceCount == 1 and myCount >= 10:
            myCount += 11

        elif aceCount != 0:
            myCount += 1

        return myCount

    @staticmethod
    @Wrappers.TimeLogger
    def createPlayinghands(myDeck):
        dealerHand = []
        playerHand = []

        dealerHand.append(myDeck.pop())

        playerHand.append(myDeck.pop())
        playerHand.append(myDeck.pop())

        if "Ass" in dealerHand:
            print("Ass")
            pass
        elif int(BlackJack_Bot.pointCount(dealerHand)) < 13:
            print("PoP")
            dealerHand.append(myDeck.pop())


        return [dealerHand, playerHand]

    @staticmethod
    @Wrappers.TimeLogger
    async def win_evaluation_bot(self, ctx, dealer, player, m, avatar, cred: int):

        chars = ["'", ","]

        for p in chars:

            if BlackJack_Bot.pointCount(dealer) == 21:
                embed = discord.Embed(
                    title='!!BLACKJACK!!',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'Der Dealer hat einen BLACKJACK!\nDir wurden: **{cred}**₹ entzogen!'
                )
                embed.set_thumbnail(url=avatar)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(player) == 21:
                embed = discord.Embed(
                    title='!!BLACKJACK!!',
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f'Du hast einen BLACKJACK!\nDir wurden: **{int(cred) * 2}**₹ überwiesen!'
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(dealer) > 21 and BlackJack_Bot.pointCount(player) > 21:
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'Ihr habt beide über 21.\nDir wurden deine Credits wieder erstattet.'
                )
                embed.set_thumbnail(url=avatar)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(dealer) > 21 > BlackJack_Bot.pointCount(player):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f'Der Dealer hat mehr als 21!\nDir wurden: **{int(cred) * 2}**₹ überwiesen!'
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(player) > 21 > BlackJack_Bot.pointCount(dealer):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'Du hast mehr als 21!\nDir wurden: **{cred}**₹ entzogen!'
                )
                embed.set_thumbnail(url=avatar)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(dealer) > BlackJack_Bot.pointCount(player):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Dp_Red),
                    description=f'Der Dealer hat mehr als du!\nDir wurden: **{cred}**₹ entzogen!'
                )
                embed.set_thumbnail(url=avatar)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(player) > BlackJack_Bot.pointCount(dealer):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Lp_Green),
                    description=f'Du hast mehr als der Dealer!\nDir wurden: **{int(cred) * 2}**₹ überwiesen!'
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "*", cred)
                return await Messaging.Universal_edit(m, embed)

            elif BlackJack_Bot.pointCount(player) == BlackJack_Bot.pointCount(dealer):
                embed = discord.Embed(
                    title='-BLACKJACK-',
                    colour=discord.Colour(Farbe.Darker_Theme),
                    description=f'Ihr habt beide gleich viel!\nDir wurden deine Credits wieder erstattet.'
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                return await Messaging.Universal_edit(m, embed)

            else:

                embed = discord.Embed(
                    title='Fehler!',
                    colour=discord.Colour(Farbe.Orange),
                    description='Ein Fehler ist in der Funktion **win_evaluation_bot** aufgetreten!\nDir wurden deine Credits wieder erstattet.'
                )
                embed.add_field(name=f'**Deine Hand: Hand:**',
                                value=f'{str(player).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(player))}')
                embed.add_field(name=f'**Dealer Hand:**',
                                value=f'{str(dealer).replace(p, " ")}\n\nGezählt:\n{str(BlackJack_Bot.pointCount(dealer))}')

                return await Messaging.Universal_edit(m, embed)


# noinspection PyTypeChecker
class SlotMachine:

    @staticmethod
    @Wrappers.TimeLogger
    async def win_evaluation_slot(self, ctx, Wheel1, Wheel2, Wheel3, m):

        if Wheel1 == Wheel2 == Wheel3:
            embed = discord.Embed(
                title="-SLOT-MASCHINE-",
                colour=discord.Colour(Farbe.Red),
                description=f"Du hast **1000**₹ gewonnen, da du den Jackpot hast!"
            )
            embed.add_field(name="1️⃣", value=f"{Wheel1}")
            embed.add_field(name="2️⃣", value=f"{Wheel2}")
            embed.add_field(name="3️⃣", value=f"{Wheel3}")

            await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "+", 1000)
            return embed

        elif Wheel1 == Wheel2 or Wheel1 == Wheel3 or Wheel2 == Wheel3:

            embed = discord.Embed(
                title="-SLOT-MASCHINE-",
                colour=discord.Colour(Farbe.Red),
                description=f"Du hast **100**₹ gewonnen, da du 2 identische Symbole hast!"
            )
            embed.add_field(name="1️⃣", value=f"{Wheel1}")
            embed.add_field(name="2️⃣", value=f"{Wheel2}")
            embed.add_field(name="3️⃣", value=f"{Wheel3}")

            await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "+", 100)
            return embed

        else:

            embed = discord.Embed(
                title="-SLOT-MASCHINE-",
                colour=discord.Colour(Farbe.Red),
                description=f"Du hast **100**₹ verloren, da du nichts gleich hast!"
            )
            embed.add_field(name="1️⃣", value=f"{Wheel1}")
            embed.add_field(name="2️⃣", value=f"{Wheel2}")
            embed.add_field(name="3️⃣", value=f"{Wheel3}")

            await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "-", 100)
            return embed
