__author__ = "Luca Michael Schmidt"

# Import
import os
import discord
from discord.ext import commands
from pymongo import MongoClient
import time


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

    initialize()
    print(f"State: |{choice}| ; Logged in as: |{client.user}| ; Latency: |{client.latency}|\n")

    Base = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Base")
    Con1 = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Connection1")
    Con2 = Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "Connection2")

    client.mongo = MongoClient(Utils.YAML.GET("Variables", "ClientSide", "MongoDB", "URL"))
    client.ticket = client.mongo[Base][Con1]
    client.Uccount = client.mongo[Base][Con2]


    print(f"\nDatabase State: |{choice}| ; Latency: |{Utils.Checker.LATENCY(client)}|")

# Cog - Initialisierung


def initialize():
    x = 0
    before = time.time()

    for filename in os.listdir('Extensions'):
        client.load_extension(f'Extensions.{filename[:-3]}') if filename.endswith(".py") else None
        x += 1

    print(f"\nFound Cogs in Extensions: |{x}|-|FOR_LOOP| ; Execution took: |{time.time() - before} seconds|")


# Token / RUN


client.run(Utils.YAML.TOKEN(5744881745535351510568150315))
