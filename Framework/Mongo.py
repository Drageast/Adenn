# Import
from typing import Optional, List
import time
import discord
import hashlib
import datetime
from .Utilities import Object


class Uccount:
    def __init__(self, client):
        self.client = client
        self.__settings = \
            {
                "Type": "default",  # Types: default, balance, shimari
                "Attributes": None,  # +, -, *
                "Timestamp": False,  # Reset Timestamp
                "Get":
                    {
                        "Return": "ALL",  # returns all information of Uccount, Types: ALL, CURRENCY, LEVELLING, SHIMARI
                        "Type": "CLASS",  # returns data as dict or class, Types: DICT, CLASS
                        "Timediff": True  # calculates Time difference
                    }
            }

        self.__example = \
            {
                "Type": "default or balance or shimari",
                "Attributes": "None, +, - or *",
                "Timestamp": "True or False",
                "Get":
                    {
                        "Return": "ALL, CURRENCY, LEVELING, SHIMARI",
                        "Type": "CLASS or DICT",
                        "Timediff": "True or False"
                    }
            }

    @property
    def exampleSettings(self):
        return self.__example

    def latency(self):
        before = time.time()
        self.client.ticket.insert_one({"_id": 1})
        after = time.time() - before
        self.client.ticket.delete_one({"_id": 1})
        return after

    @staticmethod
    def __hash(obj: str):
        return hashlib.sha1(bytes(obj, "Utf-8")).hexdigest()

    def __find(self, user: discord.Member):
        data = self.client.Uccount.find_one({"_id": self.__hash(str(user.id))})
        if data is None:
            self.__create(user)

        elif self.__hash(str(user.guild.id)) not in data:
            self.__update(user, data)

        data = self.client.Uccount.find_one({"_id": self.__hash(str(user.id))})
        return data

    def __create(self, user: discord.Member):
        epoch = datetime.datetime.utcfromtimestamp(0)
        data = {
            "_id": self.__hash(str(user.id)),

            self.__hash(str(user.guild.id)): {
                "Currency":
                    {
                        "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                        "Balance": 1000
                    },
                "Leveling":
                    {
                        "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                        "Xp": 100
                    },
                "Shimari":
                    {
                        "List": []
                    }
            }
        }

        self.client.Uccount.insert_one(data)

    def __update(self, user: discord.Member, raw: dict):
        epoch = datetime.datetime.utcfromtimestamp(0)

        if self.__hash(str(user.guild.id)) not in raw:
            data = \
                {
                    "Currency":
                        {
                            "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                            "Balance": 1000
                        },
                    "Leveling":
                        {
                            "Timestamp": (datetime.datetime.utcnow() - epoch).total_seconds(),
                            "Xp": 100
                        },
                    "Shimari":
                        {
                            "List": []
                        }
                }

            self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{self.__hash(str(user.guild.id))}": data}})

    def refactor(self, user: discord.Member, Obj, steps: List[str], settings: Optional[dict] = None):
        setting = settings if settings is not None else self.__settings
        epoch = datetime.datetime.utcfromtimestamp(0)
        path = f"{self.__hash(str(user.guild.id))}"
        path2 = f"{self.__hash(str(user.guild.id))}"
        data = self.__find(user)

        for index, step in enumerate(steps):
            path += f".{step}"
            if index < len(steps) - 1:
                path2 += f".{step}"

        if setting["Type"] == "default":
            self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path}": Obj}})
            if setting["Timestamp"] is True:
                path2 += ".Timestamp"
                self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path2}": (datetime.datetime.utcnow() - epoch).total_seconds()}})
            return

        elif setting["Type"] == "balance":
            current = data[self.__hash(str(user.guild.id))]["Currency"]["Balance"]
            new = (int(Obj) + current) if setting["Attributes"] == "+" else \
                (current - int(Obj) if setting["Attributes"] == "-" else (int(Obj) * 2) + current)
            self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path}": new}})
            if setting["Timestamp"] is True:
                path2 += ".Timestamp"
                self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path2}": (datetime.datetime.utcnow() - epoch).total_seconds()}})
            return

        elif setting["Type"] == "leveling":
            current = data[self.__hash(str(user.guild.id))]["Leveling"]["Xp"]
            new = (int(Obj) + current) if setting["Attributes"] == "+" else \
                (current - int(Obj) if setting["Attributes"] == "-" else (int(Obj) * 2) + current)
            self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path}": new}})
            if setting["Timestamp"] is True:
                path2 += ".Timestamp"
                self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {
                    "$set": {f"{path2}": (datetime.datetime.utcnow() - epoch).total_seconds()}})
            return

        elif setting["Type"] == "shimari":
            new = data[self.__hash(str(user.guild.id))]["Shimari"]["List"]
            if ("STARTER", 1) in data[self.__hash(str(user.guild.id))]["Shimari"]["List"]:
                index = new.index(("STARTER", 1))
                del new[index]

            if setting["Attributes"] == "+":
                new.append(Obj)
            if setting["Attributes"] == "-":
                index = new.index(Obj)
                del new[index]

            self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$set": {f"{path}": new}})


        else:
            raise AttributeError("Settings are incorrect! [Type] needs to be default or balance")

    def get(self, user: discord.Member, settings: Optional[dict] = None):
        setting = settings if settings is not None else self.__settings
        epoch = datetime.datetime.utcfromtimestamp(0)
        data = self.__find(user)
        data = data[self.__hash(str(user.guild.id))]
        new_List = []

        if data["Shimari"]["List"]:
            for obj in data["Shimari"]["List"]:
                New_tuple = (obj[0], obj[1])
                new_List.append(New_tuple)
            data["Shimari"]["List"] = new_List
        else:
            data["Shimari"]["List"].append(("STARTER", 1))

        if setting["Get"]["Return"] == "ALL":
            if setting["Get"]["Type"] == "DICT":
                return data
            if setting["Get"]["Type"] == "CLASS":
                obj = Object()
                obj.CTimestamp = data["Currency"]["Timestamp"] if setting["Get"]["Return"] is False else (datetime.datetime.utcnow() - epoch).total_seconds() - data["Currency"]["Timestamp"]
                obj.CBalance = data["Currency"]["Balance"]
                obj.LTimestamp = data["Leveling"]["Timestamp"] if setting["Get"]["Return"] is False else (datetime.datetime.utcnow() - epoch).total_seconds() - data["Leveling"]["Timestamp"]
                obj.LXp = data["Leveling"]["Xp"]
                obj.SList = data["Shimari"]["List"]
                return obj
            else:
                raise AttributeError("Settings are incorrect! [Get][Type] needs to be CLASS or DICT")

        if setting["Get"]["Return"] == "CURRENCY":
            if setting["Get"]["Type"] == "DICT":
                return data["Currency"]
            if setting["Get"]["Type"] == "CLASS":
                data = data["Currency"]
                obj = Object()
                obj.Timestamp = data["Timestamp"] if setting["Get"]["Return"] is False else data["Timestamp"] - (datetime.datetime.utcnow() - epoch).total_seconds()
                obj.Balance = data["Balance"]
                return obj
            else:
                raise AttributeError("Settings are incorrect! [Get][Type] needs to be CLASS or DICT")

        if setting["Get"]["Return"] == "LEVELING":
            if setting["Get"]["Type"] == "DICT":
                return data["Leveling"]
            if setting["Get"]["Type"] == "CLASS":
                data = data["Leveling"]
                obj = Object()
                obj.Timestamp = data["Timestamp"] if setting["Get"]["Return"] is False else data["Timestamp"] - (datetime.datetime.utcnow() - epoch).total_seconds()
                obj.Xp = data["Xp"]
                return obj
            else:
                raise AttributeError("Settings are incorrect! [Get][Type] needs to be CLASS or DICT")

        if setting["Get"]["Return"] == "SHIMARI":
            if setting["Get"]["Type"] == "DICT":
                return data["Shimari"]
            if setting["Get"]["Type"] == "CLASS":
                obj = Object()
                obj.List = data["Shimari"]["List"]
                return obj
            else:
                raise AttributeError("Settings are incorrect! [Get][Type] needs to be CLASS or DICT")
        else:
            raise AttributeError("Settings are incorrect! [Get][Return] needs to be ALL, CURRENCY, LEVELING or SHIMARI")

    def unset(self, user: discord.Member):
        data = self.client.Uccount.find_one({"_id": self.__hash(str(user.id))})

        if data is None:
            return

        if self.__hash(str(user.guild.id)) not in data:
            return

        self.client.Uccount.update_one({"_id": self.__hash(str(user.id))}, {"$unset": {self.__hash(str(user.guild.id)): {}}})

