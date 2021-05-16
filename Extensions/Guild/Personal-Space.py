# Import
import asyncio
import discord
from discord.ext import commands

# Framework
import Framework


# Cog Initialising


class PERSONAL(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ps"])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def create_personal_space(self, ctx, Zeit: float, name, *user: discord.Member):

        async with ctx.typing():

            rolle = await ctx.guild.create_role(name=f"{name}")

            kategorie = await ctx.guild.create_category(name)

            await kategorie.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)

            await kategorie.set_permissions(rolle, read_messages=True, send_messages=True, connect=True, speak=True)

            text = await ctx.guild.create_text_channel(f"{name}-textkanal", category=kategorie,
                                                       sync_permissions=True)
            sprach = await ctx.guild.create_voice_channel(f"{name}-sprachkanal", category=kategorie,
                                                          sync_permissions=True)

            for arg in user:
                await arg.add_roles(rolle)

            embed = discord.Embed(
                title="Fertig!",
                colour=Framework.Farbe.Lp_Green,
                description=f"Genießt den Persönlichen Bereich `{name}` nun für {Zeit} Stunden."
            )
        await Framework.Messaging.Universal_send(ctx, embed, 15)

        Zeit_converted = (((Zeit * 60) * 60) - 30)
        print(Zeit_converted)

        await asyncio.sleep(Zeit_converted)
        embed = discord.Embed(
            title="Achtung!",
            colour=Framework.Farbe.Red,
            description=f"Der Persönliche Bereich `{name}` wird in **30 Sekunden gelöscht**!"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        for arg in user:
            x = await arg.send(embed=embed)

        await asyncio.sleep(30)
        await text.delete()
        await sprach.delete()
        await kategorie.delete()
        await rolle.delete()
        await x.delete()


# COG_SETUP(END)


def setup(client):
    client.add_cog(PERSONAL(client))
