# Import
import asyncio
import datetime
import traceback
from datetime import datetime
import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class HANDLER(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ERROR_HANDLER

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Dieser Command ist Deaktiviert.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await ctx.message.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await m.delete()

        elif isinstance(error, commands.NoPrivateMessage):

            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Du darfst diesen Command nicht in Privatnachrichten nutzen.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.BadArgument or commands.ArgumentParsingError or commands.BadBoolArgument):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Dein angegebenes Argument ist fehlerhaft.\n`{error}`'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.MissingRequiredArgument or commands.TooManyArguments):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Dein angegebenes Argument ist fehlerhaft.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.MissingPermissions or commands.BotMissingPermissions):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du besitzt nicht die benötigten Rechte ({error.missing_perms}), andernfalls besitze ich nicht die benötigten Rechte!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Hey! Was machst du da?',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Du kannst mich mit diesem Befehl __stark beschädigen__!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.CommandOnCooldown):

            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du **musst {"%.2f" % round(error.retry_after, 2)}sek. warten**, bevor du den Command erneut benutzen kannst'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Hey! Was machst du da?',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du erfüllst nicht die benötigten Rechte.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:

                await ctx.message.delete()
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

            except discord.HTTPException:

                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                await m.delete()

        elif isinstance(error, commands.CommandInvokeError):

            if isinstance(error.original, Utils.CreditError):

                embed = discord.Embed(
                    title='',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{error.__context__}'
                )
                embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))
                embed.set_thumbnail(url=self.client.user.avatar_url)

                try:

                    await ctx.message.delete()
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()

                except discord.HTTPException:

                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()
                return

            elif isinstance(error.original, Utils.MusicError):

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'Etwas in der Rubrik: `Enhanced Music` ist schiefgelaufen. Versuche es erneut.\n`{error}`'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                try:

                    await ctx.message.delete()
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()

                except discord.HTTPException:

                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()
                return

            if isinstance(error.original, Utils.UccountError):

                embed = discord.Embed(
                    title='-Uccount-',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{error.__context__}'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                try:

                    await ctx.message.delete()
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()

                except discord.HTTPException:

                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    await m.delete()
                return

            else:

                embed = discord.Embed(
                    title='ACHTUNG!',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description='Der Command ist **korrumpiert**!\nTritt dieser Fehler erneut auf, '
                                'kontaktiere **dringend** den Support: **!s**'
                )
                embed.add_field(name='**LOG:**', value=f'```css\n[{error}]\n```')
                embed.set_thumbnail(url=self.client.user.avatar_url)

                async with aiohttp.ClientSession() as session:
                    url = "https://discordapp.com/api/webhooks/815708355371860069/gy3_edx9paMdTg6f-0WL2qOlWnGKalV_10SPwK3jjdWV3f4dPSbvLStyDmClkAVQBRgu"

                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

                    timestamp = datetime.utcnow()
                    trace = traceback.format_exception(None, error, error.__traceback__)
                    b = 0

                    erembed = discord.Embed(
                        title="\u200b\nEin schwerwiegender Fehler ist aufgetreten!\n\u200b",
                        colour=discord.Colour(Utils.Farbe.Red)
                    )
                    erembed.set_author(name=f"{timestamp.strftime(r'%I:%M %p')}",
                                       icon_url=Utils.YAML.GET("Bilder", "Clock"))
                    erembed.add_field(name='**OPERATOR:**', value=f'```fix\n[{ctx.author} / {ctx.author.id}]\n```',
                                      inline=False)
                    try:
                        erembed.add_field(name='**SERVER:**', value=f'```fix\n[{ctx.guild.name}]\n```', inline=False)
                        erembed.add_field(name='**KANAL:**', value=f'```fix\n[{ctx.channel.name}]\n```', inline=False)
                    except AttributeError:
                        pass
                    erembed.add_field(name='**COMMAND:**',
                                      value=f'```fix\n[{self.client.command_prefix}{ctx.command.qualified_name}]\n```',
                                      inline=False)
                    erembed.add_field(name='**NACHRICHT:**', value=f'```fix\n[{ctx.message.content}]\n```',
                                      inline=False)
                    erembed.add_field(name='**ERROR:**', value=f'```css\n[{error}]\n```\n\n\u200b', inline=False)
                    erembed.add_field(name='**TRACEBACK:**', value=f'\u200b', inline=False)
                    erembed.set_thumbnail(url=self.client.user.avatar_url)
                    for _ in trace:
                        erembed.add_field(name='\u200b', value=f'```python\n{trace[b]}\n```', inline=False)
                        b += 1

                    await webhook.send(username="Ein korrumpierter Command wurde ausgelöst!",
                                       avatar_url=self.client.user.avatar_url, embed=erembed)

                    try:

                        await ctx.message.delete()
                        m = await ctx.send(embed=embed)
                        await asyncio.sleep(15)
                        await m.delete()

                    except discord.HTTPException:

                        m = await ctx.send(embed=embed)
                        await asyncio.sleep(15)
                        await m.delete()

    # COMMAND_HANDLER

    @staticmethod
    def check_command(self, command_name):
        command = self.client.get_command(command_name)

        choice = '```json\n"AKTIV"\n```' if command.enabled else '```fix\n"INAKTIV"\n```'

        return choice

    @commands.command(aliases=["ds"])
    @commands.is_owner()
    async def disable_commands(self, ctx, *, command_name):

        if command_name is not None:

            command = self.client.get_command(command_name)

            if command is None:

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'Dieser Command existiert nicht.\nÜberprüfe ihn auf Rechtschreibfehler.\nDeine Angabe: **{command_name}**'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.SMOOTH.Embed_ctx(ctx, embed, 30)


            elif command == ctx.command:

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'Du darfst diesen Command nicht Deaktivieren!'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.SMOOTH.Embed_ctx(ctx, embed, 30)

            else:

                command.enabled = not command.enabled

                choice = "Aktiviert" if command.enabled else "Deaktiviert"
                choice_colour = Utils.Farbe.Lp_Green if command.enabled else Utils.Farbe.Dp_Red

                embed = discord.Embed(
                    title=f'{choice}',
                    colour=discord.Colour(choice_colour),
                    description=f'Der Command: **{command}** wurde erfolgreich {choice}.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.SMOOTH.Embed_ctx(ctx, embed, 10)


# Cog Finishing


def setup(client):
    client.add_cog(HANDLER(client))
