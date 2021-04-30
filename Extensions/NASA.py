# Import
from datetime import datetime

import discord
import requests
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class NASA(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(aliases=["na"], invoke_without_command=True)
    async def NASA(self, ctx):

        embed = discord.Embed(
            title="NASA",
            colour=discord.Colour(Utils.Farbe.Lp_Blue),
            description=f"Dies ist die **NASA Gruppe**.\nGebe: `{self.client.command_prefix}nasa Command` ein.\n Command: - **ap**n"
        )
        embed.set_thumbnail(url=f'{Utils.YAML.GET("Bilder", "NASA")}')
        await Utils.Messaging.Universal_send(ctx, embed)

    # PICTURE_OF_THE_DAY

    @NASA.group(aliases=['ap'])
    async def Astr_pic_day(self, ctx):
        url = f"https://api.nasa.gov/planetary/apod?api_key={str(Utils.YAML.GET('Variables', 'API', 'NASA'))}"

        data = requests.get(url).json()

        pic_url = data["url"]
        datum = data["date"]
        datum = datum.replace("-", "/")
        datum = datetime.strptime(datum, "%Y/%m/%d")
        try:
            copy_right = data["copyright"]
        except:
            copy_right = "None"
        title = data["title"]
        description = data["explanation"]

        embed = discord.Embed(
            title=f"Astronomic Picture of the Day: {title}",
            colour=discord.Colour(Utils.Farbe.Lp_Blue),
            description=f"{description}\n**URL:** _{pic_url}_",
            timestamp=datum
        )
        embed.set_thumbnail(url=f'{Utils.YAML.GET("Bilder", "NASA")}')
        embed.set_image(url=f"{pic_url}")
        embed.set_footer(text=f"Copyright: {copy_right} | ")

        await Utils.Messaging.Universal_send(ctx, embed, 30)


# Cog Finishing


def setup(client):
    client.add_cog(NASA(client))
