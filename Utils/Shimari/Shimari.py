from Utils.Utilities import Wrappers, Farbe, Messaging
from Utils.ErrorHandler import YAMLError
from Utils.MongoDataBase import Uccounts
import yaml
import discord
from discord.ext import commands
import random
import asyncio


class YAML:

    @staticmethod
    @Wrappers.TimeLogger
    def PATH(container: str):
        try:
            with open("Utils/Shimari/config.yaml", "r") as f:
                container_ = yaml.safe_load(f)
            container_ = container_[container]
            return container_
        except Exception as e:
            raise YAMLError(e)

    @staticmethod
    @Wrappers.TimeLogger
    def GET(Container: str, *Load: str or int):
        try:
            dict_ = YAML.PATH(Container)
            new_dict = dict_
            for load in Load:
                new_dict = new_dict[load]

            return new_dict
        except Exception as e:
            raise YAMLError(e)

    @staticmethod
    @Wrappers.TimeLogger
    def UNPACK(ID):
        try:
            with open("Utils/Shimari/ShimariData.yaml", "r") as f:
                container = yaml.safe_load(f)
        except Exception as e:
            raise YAMLError(e)

        if ID == "List":
            List = container["Control"]
            return List

        else:

            try:
                raw_Shimari = container["ID"][ID]

                UnPacked = Object()
                UnPacked.Name = raw_Shimari["Name"]
                UnPacked.Motto = raw_Shimari["Motto"]
                UnPacked.Avatar = raw_Shimari["Avatar"]
                UnPacked.Mana = raw_Shimari["KDTN"]["Mana"]
                UnPacked.Kosten = raw_Shimari["KDTN"]["Kosten"]
                UnPacked.Leben = raw_Shimari["KDTN"]["Leben"]
                UnPacked.Schaden = raw_Shimari["KDTN"]["Schaden"]
                UnPacked.Element = raw_Shimari["KDTN"]["Element"][0]
                UnPacked.Element_Resistenz = raw_Shimari["KDTN"]["Element"][1]
                UnPacked.Seltenheit = raw_Shimari["KDTN"]["Seltenheit"]

                return UnPacked

            except:

                raise YAMLError("Die angegebene ID ist ungültig!")


class Object(object):
    pass


class ShimariBASE:

    @Wrappers.TimeLogger
    def __init__(self, ID: int):
        self.Data = YAML.UNPACK(ID)
        self.ID = ID
        self.Name: str = self.Data.Name
        self.Motto: str = self.Data.Motto
        self.Avatar: str = self.Data.Avatar
        self.Mana: int = self.Data.Mana
        self.Cost: list = self.Data.Kosten
        self.Damage: list = self.Data.Schaden
        self.Health: int = self.Data.Leben
        self.Element: str = self.Data.Element
        self.Resistance: str = self.Data.Element_Resistenz
        self.Rarity: int = self.Data.Seltenheit
        self.Operator: str = "Player"

        while "1" in self.Motto:
            self.Motto = self.Motto.replace("1", "ä")
        while "2" in self.Motto:
            self.Motto = self.Motto.replace("2", "ö")
        while "3" in self.Motto:
            self.Motto = self.Motto.replace("3", "ü")

    def __str__(self):
        return f"\n`Name`: _{self.Name}_\n`Motto`:\n_{self.Motto}_\n`Mana`: _{self.Mana}_\n`Angriffskosten`: _{self.Cost}_" \
               f"\n`Schaden`: _{self.Damage}_\n`Leben`: _{self.Health}_\n`Element`: _{self.Element}_\n`Resistenz`: _{self.Resistance}_\n`Seltenheit`: **{self.GetRarity()}**\n"

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def debug(self):
        x = [{"Name": self.Name, "Motto": self.Motto},
             {"KDTN": {"Mana": self.Mana, "Kosten": self.Cost, "Schaden": self.Damage, "Leben": self.Health}},
             {"KDTN": {"Element": self.Element, "Resistenz": self.Resistance}},
             {"KDTN": {"Seltenheit - Integer": self.Rarity, "Seltenheit - String": self.GetRarity()}}]
        return x

    def GetRarity(self):
        return "Exotisch" if self.Rarity == 4 else (
            "Legendär" if self.Rarity == 3 else ("Selten" if self.Rarity == 2 else "Normal"))

    def fight_data(self, damage=None):
        y = f"\n`Schaden`: {damage}" if damage is not None else ""
        x = f"`Leben`: {self.Health}\n`Mana`: {self.Mana}{y}"
        return x

    def post_fight_data(self):
        return f"`Mana`: {self.Mana}\n`Angriffskosten`: {self.Cost}\n`Angriffsschaden`: {self.Damage}"

    def price(self):
        base_price = YAML.GET("Shop", "Preis")
        return base_price[3] if self.Rarity == 4 else (
            base_price[2] if self.Rarity == 3 else (base_price[1] if self.Rarity == 2 else base_price[0]))

    def avatar(self):
        return self.Avatar[(int(self.Rarity) - 1)]

    def random_Energie(self):
        rnum = random.randint(YAML.GET("Random_Energie", "Start"), YAML.GET("Random_Energie", "End"))

        if self.Rarity == 4:
            bonus = YAML.GET("Random_Energie", "Bonus")[3]
        if self.Rarity == 3:
            bonus = YAML.GET("Random_Energie", "Bonus")[2]
        if self.Rarity == 2:
            bonus = YAML.GET("Random_Energie", "Bonus")[1]
        if self.Rarity == 1:
            bonus = YAML.GET("Random_Energie", "Bonus")[0]

        self.Mana += int(rnum + bonus)

    @Wrappers.TimeLogger
    def update_Stats(self):
        print(self.Health, self.Data.Leben)
        if self.Health == self.Data.Leben:
            if self.Rarity == 1:
                self.Health = (int(self.Data.Leben + int(YAML.GET("Update_Stats", 1)[0])))
                self.Mana = (int(self.Data.Mana + int(YAML.GET("Update_Stats", 1)[1])))
                print("Stufe 1")
                return
            elif self.Rarity == 2:
                self.Health = (int(self.Data.Leben + int(YAML.GET("Update_Stats", 2)[0])))
                self.Mana = (int(self.Data.Mana + int(YAML.GET("Update_Stats", 2)[1])))
                print("Stufe 2")
                return
            elif self.Rarity == 3:
                self.Health = (int(self.Data.Leben + int(YAML.GET("Update_Stats", 3)[0])))
                self.Mana = (int(self.Data.Mana + int(YAML.GET("Update_Stats", 3)[1])))
                print("Stufe 3")
                return
            elif self.Rarity == 4:
                self.Health = (int(self.Data.Leben + int(YAML.GET("Update_Stats", 4)[0])))
                self.Mana = (int(self.Data.Mana + int(YAML.GET("Update_Stats", 4)[1])))
                print("Stufe 4")
                return

        else:
            print("ELSE")
            return

    @Wrappers.TimeLogger
    def tuple_Shimari(self):
        x = (self.ID, self.Rarity)
        return x


class Shimari(ShimariBASE):


    @staticmethod
    @Wrappers.TimeLogger
    def fight(Shimari1: ShimariBASE, Shimari2: ShimariBASE, Attack: int):
        Chance = random.randint(1, 10)

        bonus = YAML.GET("Bonus_Stats", "Resistance") if Shimari1.Element == Shimari2.Resistance else \
            (YAML.GET("Bonus_Stats", 1) if Attack == 1 else (
                YAML.GET("Bonus_Stats", 2) if Attack == 2 else YAML.GET("Bonus_Stats", 3)))

        Health = int(Shimari2["Health"]) - (int(Shimari1["Damage"][Attack - 1]) + int(bonus))

        Energie = int(Shimari1["Mana"]) - int(Shimari1["Cost"][Attack - 1])

        Shimari1["Mana"] = Energie

        if Chance <= int(Shimari2.Rarity):
            data = Object()
            data.damage = "Geblockt!"

            return data

        else:

            Shimari2["Health"] = Health
            data = Object()
            data.damage = int(Shimari1["Damage"][Attack - 1]) + int(bonus)

            return data


class DiscordShimari:

    @staticmethod
    @Wrappers.TimeLogger
    def GET_randomShimari():
        shimari = random.choice(YAML.UNPACK("List"))

        Shimari_ = YAML.UNPACK(shimari)

        Rarity = random.randint(1, Shimari_.Seltenheit)
        control = random.randint(1, YAML.GET("Random_Rarity", "Max_Chance"))

        while control < YAML.GET("Random_Rarity", "Control") and Rarity == 4:
            Rarity = random.randint(1, Shimari_.Seltenheit)

        tpl = (shimari, Rarity)

        return tpl

    @staticmethod
    @Wrappers.TimeLogger
    def list_control(name=None):
        Name = name if name else None
        if Name:
            if "_" in Name:
                Name = Name.replace("_", " ")

        control = YAML.UNPACK("List")

        shimaris = []

        for index, obj in enumerate(control):
            x = (obj, 1)
            x = DiscordShimari.Create_Shimari(x)

            if Name:
                if x.Name.lower() == Name.lower():
                    shimaris.append(x)
            else:
                shimaris.append(x)

        if not shimaris:
            raise commands.BadArgument("Das Angegebene Shimari existiert nicht!")
        return shimaris

    @staticmethod
    @Wrappers.TimeLogger
    def Create_Shimari(Shimari_: tuple):
        ID, Rarity = Shimari_

        x = Shimari(ID)

        x["Rarity"] = Rarity
        x.update_Stats()

        return x

    @staticmethod
    @Wrappers.TimeLogger
    def CALCULATE_Attack(Shimari_: ShimariBASE):
        S = Shimari_

        if S.Mana >= (S.Cost[2]):
            return 3

        elif S.Mana >= (S.Cost[1] ):
            return 2

        elif S.Mana >= (S.Cost[0]):
            return 1

        else:

            return 1

    @staticmethod
    async def ShimariShop(self, ctx, content: list, shimari_list: list, info: str = None):

        contents = content

        info_ = None

        pages = len(contents)

        cur_page = 0
        try:
            await ctx.message.delete()
        except:
            pass

        message = await ctx.send(embed=contents[cur_page])

        await message.add_reaction("◀️")
        await message.add_reaction("⏹️")
        await message.add_reaction("▶️")
        await message.add_reaction("💶")
        if info is not None:
            await message.add_reaction("ℹ️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "⏹️", "▶️", "ℹ️", "💶", "✔", "❌"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

                if str(reaction.emoji) == "▶️":
                    if cur_page != pages - 1:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page])
                        await message.remove_reaction(reaction, user)
                    else:
                        pass

                elif str(reaction.emoji) == "◀️" and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    try:
                        await message.delete()
                    except:
                        pass
                    try:
                        await info_.delete()
                    except:
                        pass
                    break

                elif str(reaction.emoji) == "ℹ️":
                    if info_ is None:
                        info_ = await ctx.send(info)
                    else:
                        try:
                            await info_.delete()
                        except:
                            pass
                        info_ = None

                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "💶":

                    Shimari_ = DiscordShimari.Create_Shimari(shimari_list[cur_page])

                    embed = discord.Embed(
                        title=":~Shop~:",
                        colour=discord.Colour(Farbe.ShimariRosa),
                        description=f"Möchtest du das Shimari: **{Shimari_.Name}** für **{Shimari_.price()}**₹ verkaufen?"
                    )
                    embed.set_image(url=Shimari_.avatar())

                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await message.add_reaction("✔")
                    await message.add_reaction("❌")

                if str(reaction.emoji) == "✔":
                    embed = discord.Embed(
                        title=":~Shop~:",
                        colour=discord.Colour(Farbe.ShimariRosa),
                        description=f"Du hast das Shimari: **{Shimari_.Name}** für **{Shimari_.price()}**₹ verkauft."
                    )
                    embed.set_image(url=Shimari_.avatar())

                    await Uccounts.update_Shimari(self, ctx, ctx.author.id, shimari_list[cur_page], "-")
                    await Uccounts.currencyUp_Uccount(self, ctx, ctx.author.id, "+", DiscordShimari.Create_Shimari(shimari_list[cur_page]).price())
                    await Messaging.Universal_edit(message, embed)
                    break

                elif str(reaction.emoji) == "❌":
                    try:
                        await message.delete()
                    except:
                        pass
                    break

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except:
                    pass
                try:
                    await info_.delete()
                except:
                    pass
                break

    @staticmethod
    @Wrappers.TimeLogger
    def failure_chance():
        rnum = random.randint(1, 100)
        rnum2 = random.randint(1, 2)

        if rnum < YAML.GET("Failure_Rate", "Buttons"):
            print("Failure")
            return rnum2
        return 0

