# Import
import discord
from discord.ext import commands


# Utils
import Utils


# Cog Initialising


class HILFE(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.commands_pepa = 5


    @staticmethod
    @Utils.Wrappers.TimeLogger
    def get_command_signature(command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name} oder: {aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}  {cmd_invoke}  {command.signature}"
        return signature


    @commands.command(aliases=["test"])
    @Utils.Wrappers.TimeLogger
    async def hilfe(self, ctx):
        pass


# Cog Finishing


def setup(client):
    client.add_cog(HILFE(client))
