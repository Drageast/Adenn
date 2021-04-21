from Utils.Utilities import Wrappers
from Utils.ErrorHandler import YAMLError
import yaml


@Wrappers.TimeLogger
def UNPACK(ID):
    with open("test.yaml", "r") as f:
        container = yaml.safe_load(f)
    try:
        int(ID)
        raw_Shimari = container["ID"][ID]

        UnPacked = Object()
        UnPacked.Name = raw_Shimari["Name"]
        UnPacked.Description = raw_Shimari["Description"]
        UnPacked.Avatar = raw_Shimari["URL"]["Avatar"]
        UnPacked.Energie = raw_Shimari["Data"]["BasisEnergie"]
        UnPacked.Angriffskosten = raw_Shimari["Data"]["Angriffskosten"]
        UnPacked.Leben = raw_Shimari["Data"]["Leben"]
        UnPacked.Schaden = raw_Shimari["Data"]["Schaden"]
        UnPacked.Element = raw_Shimari["Data"]["Element"]
        UnPacked.Element_Resistenz = raw_Shimari["Data"]["Resistenz"]
        UnPacked.Seltenheit = raw_Shimari["Data"]["Seltenheit"]

        return UnPacked

    except:

        if ID == "List":
            List = container["Control"]
            return List

        else:
            raise YAMLError("Die angegebene ID ist ungültig!")


class Object(object):
    pass


class ShimariBASE:


    @Wrappers.TimeLogger
    def __init__(self, ID: int):
        self.Shimari = UNPACK(ID)
        self.ID = ID
        self.Name: str = self.Shimari.Name
        self.Description: str = self.Shimari.Description
        self.Avatar: str = self.Shimari.Avatar
        self.BaseEnergie: int = self.Shimari.Energie
        self.AttackCost: list = self.Shimari.Angriffskosten
        self.Damage: list = self.Shimari.Schaden
        self.Health: int = self.Shimari.Leben
        self.Element: str = self.Shimari.Element
        self.Resistance: str = self.Shimari.Element_Resistenz
        self.Rarity: int = self.Shimari.Seltenheit

    def __str__(self):
        return f"```\nName: {self.Name}\nBeschreibung: {self.Description}\nBasis Energie: {self.BaseEnergie}\nAngriffskosten: {self.AttackCost}" \
               f"\nSchaden: {self.Damage}\nLeben: {self.Health}\nElement: {self.Element}\nResistenz: {self.Resistance}\nSeltenheit: {self.GetRarity()}\n```"

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def GetRarity(self):
        return "Exotisch" if self.Rarity == 4 else ("Legendär" if self.Rarity == 3 else ("Selten" if self.Rarity == 2 else "Normal"))


class Shimari(ShimariBASE):

    @staticmethod
    @Wrappers.TimeLogger
    def fight(Shimari1: ShimariBASE, Shimari2: ShimariBASE, Attack: int):

        if int(Shimari2["Health"]) <= 0:
            return False

        elif int(Shimari1["BaseEnergie"]) < 1:
            return False

        else:

            bonus = 0 if Shimari1.Element == Shimari2.Resistance else (0 if Attack == 1 else (20 if Attack == 2 else 30))
            Health = int(Shimari2["Health"]) - (int(Shimari1["Damage"][Attack - 1]) + int(bonus))
            Energie = int(Shimari1["BaseEnergie"]) - int(Shimari1["AttackCost"][Attack - 1])

            Shimari2["Health"] = Health
            Shimari1["BaseEnergie"] = Energie
            print(Health, Energie, (int(Shimari1["Damage"][Attack - 1]) + int(bonus)))
            return True
