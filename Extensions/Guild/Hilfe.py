# Import
import discord
from discord.ext import commands


# Framework
import Framework


# Cog Initialising


class MyHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '`%s%s %s`' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=Framework.Farbe.Orange)
            try:
                await destination.send(embed=emby, delete_after=25)
            except:
                continue

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=self.get_command_signature(command))
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        try:
            await channel.send(embed=embed, delete_after=25)
        except:
            return


class HILFE(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.help_command = MyHelp()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("!help"):
            await message.delete()


# Cog Finishing


def setup(client):
    client.add_cog(HILFE(client))
