__author__ = "Luca Michael Schmidt"
__version__ = "4.01"


# Import
import os
import discord
from discord.ext import commands
from pymongo import MongoClient


# Utils
import Utils


# Client Setup
intents = discord.Intents.all()
intents.members = True
client = commands.AutoShardedBot(command_prefix=Utils.YAML.GET("Variables", "ClientSide", "Prefix"), intents=intents, case_insensitive=True)


# MongoDB Initialisierung

@client.listen()
@Utils.Wrappers.TimeLogger
async def on_ready():

    State = Utils.YAML.GET("Variables", "ClientSide", "Status")
    choice = "ONLINE" if State == 1 else "WARTUNG"
    choicemessage = "Das ist der Weg!" if State == 1 else "Maintenance Mode"
    choicestatus = discord.Status.online if State == 1 else discord.Status.do_not_disturb
    client.State = State

    await client.change_presence(status=choicestatus, activity=discord.Game(choicemessage))
    try:
        await initialize()
    except commands.ExtensionAlreadyLoaded:
        pass
    print(f"\nState: |{choice}| ; Logged in as: |{client.user}| ; Latency: |{client.latency}|\n")

    Base = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Base")
    Con1 = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Connection1")
    Con2 = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Connection2")

    client.mongo = MongoClient(Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "URL"))
    client.ticket = client.mongo[Base][Con1]
    client.Uccount = client.mongo[Base][Con2]


    print(f"\nDatabase State: |{choice}| ; Latency: |{Utils.Checker.LATENCY(client)}|\n")


# Cog - Initialisierung


async def initialize():

    await Utils.Shimari.YAMLShi.Update("config.yaml")
    await Utils.Shimari.YAMLShi.Update("ShimariData.yaml")

    print(f"\nSuccess -|REQUEST| ; Pulled from: |GitHub - Drageast|\n")


    for filename in os.listdir('Extensions'):
        if os.path.isfile(f"Extensions/{filename}"):
            if filename.endswith(".py") and not filename.startswith("__") and not filename.endswith(".pyc"):
                try:
                    client.load_extension(f'Extensions.{filename[:-3]}')
                    print(f"Loaded Extension: |{filename}|")
                except Exception as e:
                    print(f"ERROR Loading Extension: |{filename}| ; Error: |{e}|")
                    continue
        else:
            for filename2 in os.listdir(f"Extensions/{filename}"):
                if filename2.endswith(".py") and not filename2.startswith("__") and not filename2.endswith(".pyc"):
                    try:
                        client.load_extension(f'Extensions.{filename}.{filename2[:-3]}')
                        print(f"Loaded Extension: |{filename}.{filename2}|")
                    except Exception as e:
                        print(f"ERROR Loading Extension: |{filename}.{filename2}| ; Error: |{e}|")
                        continue


# Token / RUN


client.run(Utils.YAML.TOKEN(5744881745535351510568150315))
