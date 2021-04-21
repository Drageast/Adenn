# Import
import datetime
import time
from datetime import date
from .ErrorHandler import UccountError
from .Utilities import Wrappers
from .Utilities import Object


class Uccounts:


    @staticmethod
    @Wrappers.TimeLogger
    def Operation(Operator, BalUpdate: int, CurrentBal: int):
        if Operator == "-":

            NewBal: int = int(CurrentBal) - int(BalUpdate)
            return NewBal

        elif Operator == "+":

            NewBal: int = int(CurrentBal) + int(BalUpdate)
            return NewBal

        elif Operator == "*":

            NewBal: int = int(CurrentBal) + (int(BalUpdate) * 2)
            return NewBal

        elif Operator == "/":

            NewBal: int = round(int(CurrentBal) + (int(BalUpdate) / 2))
            return NewBal

        else:
            raise UccountError("Der Operator für `Casino.Balance` ist fehlerhaft!")


    @staticmethod
    @Wrappers.TimeLogger
    async def check_Uccount(self, ctx, Uid_, Index: int = None):

        epoch = datetime.datetime.utcfromtimestamp(0)

        Uid = f"{Uid_}:{ctx.guild.id}"

        Uccount = self.client.Uccount.find_one({"_id": Uid})


        if Index == 1:

            if Uccount is None:
                await Uccounts.create_Uccount(self, ctx, Uid_)

            data = self.client.Uccount.find_one({"_id": Uid})

            data = data["Casino"]

            data_ = Object()

            data_.diff = int((datetime.datetime.utcnow() - epoch).total_seconds() - int(data["Timestamp"]))
            data_.lock = data["Lock"]
            data_.bal = data["Balance"]
            data_.role = data["Specified_Role"]

            return data_

        elif Index == 2:

            if Uccount is None:
                await Uccounts.create_Uccount(self, ctx, Uid_)

            data = self.client.Uccount.find_one({"_id": Uid})

            data = data["Leveling"]

            data_ = Object()

            data_.diff = (datetime.datetime.utcnow() - epoch).total_seconds() - int(data["Timestamp"])
            data_.xp = data["Xp"]

            return data_

        elif Index == 3:

            if Uccount is None:
                await Uccounts.create_Uccount(self, ctx, Uid_)

            data = self.client.Uccount.find_one({"_id": Uid})

            data = data["Main"]

            data_ = Object()

            data_.name = data["Name"]
            data_.server = data["Server"]
            data_.verlauf = data["Verlauf"]

            return data_

        elif Index == 4:

            if Uccount is None:
                await Uccounts.create_Uccount(self, ctx, Uid_)

            data = self.client.Uccount.find_one({"_id": Uid})

            data = data["ShimariBASE"]

            data_ = Object()

            data_.ShimariList = data["List"]

            return data_

        elif Index is None:

            if Uccount is None:
                return False

            else:
                return True

    @staticmethod
    @Wrappers.TimeLogger
    async def create_Uccount(self, ctx, Uid_):

        epoch = datetime.datetime.utcfromtimestamp(0)
        today = date.today()

        Uid = f"{Uid_}:{ctx.guild.id}"

        Uccount = self.client.Uccount.find_one({"_id": Uid})

        name = await self.client.fetch_user(Uid_)


        if Uccount is None:

            data = \
                {
                    "_id": Uid,
                    "Casino": {
                        "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                        "Lock": False,
                        "Specified_Role": False,
                        "Balance": 5000
                    },
                    "Leveling": {
                        "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                        "Xp": 10
                    },
                    "Main": {
                        "CreateTime": today.strftime("%d/%m"),
                        "Name": name.name,
                        "Server": ctx.guild.name,
                        "Verlauf": 0
                    },
                    "Shimari": {
                        "List": []
                    }
                }

            self.client.Uccount.insert_one(data)

        else:

            raise UccountError(f"Der Uccount von `|{Uid}|` existiert bereits!")


    @staticmethod
    @Wrappers.TimeLogger
    async def update_Uccount(self, ctx, Uid_, Index: str, Element: str, OBJ):

        Uid = f"{Uid_}:{ctx.guild.id}"

        Uccount = self.client.Uccount.find_one({"_id": Uid})

        if Uccount is None:

            await Uccounts.create_Uccount(self, ctx, Uid_)

        try:
            self.client.Uccount.update_one({"_id": Uid}, {"$set": {f"{Index}.{Element}": OBJ}})

        except:
            raise UccountError("Bei dem Update ist etwas schiefgelaufen!\n `{'_id': "f"{Uid}""}, {'$set': {'"f"{Index}.{Element}': "f"{OBJ}}}`")


    @staticmethod
    @Wrappers.TimeLogger
    async def currencyUp_Uccount(self, ctx, Uid_, Operator, BalUpdate: int):

        Uid = f"{Uid_}:{ctx.guild.id}"

        Uccount = self.client.Uccount.find_one({"_id": Uid})

        if Uccount is None:
            await Uccounts.create_Uccount(self, ctx, Uid_)

        data = await Uccounts.check_Uccount(self, ctx, Uid_, 1)

        CurrentBal = int(data.bal)

        NewBal = Uccounts.Operation(Operator, BalUpdate, CurrentBal)
        self.client.Uccount.update_one({"_id": Uid}, {"$set": {"Casino.Balance": NewBal}})

    @staticmethod
    @Wrappers.TimeLogger
    async def update_Shimaris(self, ctx, Uid_, Shimari: tuple, Operator: str):

        if Operator == "+":

            data = await Uccounts.check_Uccount(self, ctx, Uid_, 4)
            new_List = data.ShimariList

            if Shimari in new_List:
                ID1, Rarity1 = Shimari
                ID2, Rarity2 = new_List[new_List.index(Shimari)]
                if Rarity1 < Rarity2:
                    return False

                else:
                    new_List.append(Shimari)

            else:
                new_List.append(Shimari)

        elif Operator == "-":

            data = await Uccounts.check_Uccount(self, ctx, Uid_, 4)
            new_List = data.ShimariList
            index = new_List.index(Shimari)

            print(f"Das Shimari {Shimari} ist an Stelle {index}")
            del new_List[index]


        Uid = f"{Uid_}:{ctx.guild.id}"
        self.client.Uccount.update_one({"_id": Uid}, {"$set": {"Shimari.List": new_List}})
