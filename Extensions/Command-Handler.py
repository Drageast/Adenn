# Import
import traceback
from datetime import datetime
import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
import psutil


# Utils
import Utils


# Cog Initialising


class HANDLER(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ERROR_HANDLER

    @commands.Cog.listener()
    @Utils.Wrappers.TimeLogger
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Dieser Command ist Deaktiviert.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.NoPrivateMessage):

            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Du darfst diesen Command nicht in Privatnachrichten nutzen.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.BadArgument or commands.ArgumentParsingError or commands.BadBoolArgument):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Dein angegebenes Argument ist fehlerhaft.\n`{error}`'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.MissingRequiredArgument or commands.TooManyArguments):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Dein angegebenes Argument ist fehlerhaft.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.MissingPermissions or commands.BotMissingPermissions):
            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du besitzt nicht die benötigten Rechte ({error.missing_perms}), andernfalls besitze ich nicht die benötigten Rechte!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Hey! Was machst du da?',
                colour=discord.Colour(Utils.Farbe.Red),
                description='Du kannst mich mit diesem Befehl __stark beschädigen__!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.CommandOnCooldown):

            embed = discord.Embed(
                title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du **musst {"%.2f" % round(error.retry_after, 2)}sek. warten**, bevor du den Command erneut benutzen kannst'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Hey! Was machst du da?',
                colour=discord.Colour(Utils.Farbe.Red),
                description=f'Du erfüllst nicht die benötigten Rechte.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Utils.Messaging.Universal_send(ctx, embed, 15)

        elif isinstance(error, commands.CommandInvokeError):

            if isinstance(error.original, Utils.CreditError):

                embed = discord.Embed(
                    title='',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{error.__context__}'
                )
                embed.set_author(name="Credit Bank", icon_url=Utils.YAML.GET("Bilder", "Credits"))
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)

            elif isinstance(error.original, Utils.MusicError):

                embed = discord.Embed(
                    title=f'{Utils.YAML.GET("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'Etwas in der Rubrik: `Enhanced Music` ist schiefgelaufen. Versuche es erneut.\n`{error}`'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)

            if isinstance(error.original, Utils.UccountError):

                embed = discord.Embed(
                    title='-Uccount-',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f'{error.__context__}'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.Messaging.Universal_send(ctx, embed, 15)

            else:

                embed = discord.Embed(
                    title='ACHTUNG!',
                    colour=discord.Colour(Utils.Farbe.Red),
                    description='In diesem Command ist ein schwerwiegender Fehler aufgetreten!\nIch habe die Fehlermeldung and das Developement Team weitergeleitet.'
                                'Tritt dieser Fehler in den nächsten Tagen erneut auf, '
                                'kontaktiere **dringend** den Support: **!s**'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                async with aiohttp.ClientSession() as session:
                    url = Utils.YAML.GET("Variables", "ClientSide", "Webhooks", "System")

                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))


                    trace = traceback.format_exception(None, error, error.__traceback__)
                    if '\nThe above exception was the direct cause of the following exception:\n\n' in trace:
                        trace = trace[:trace.index('\nThe above exception was the direct cause of the following exception:\n\n')]
                        traceback_text = "\n".join(trace)
                    else:
                        traceback_text = trace

                    y = 0
                    for obj in traceback_text:
                        y += len(obj)

                    while y >= 2045:
                        traceback_text = traceback_text[:1]
                        y = 0
                        for obj in traceback_text:
                            y += len(obj)

                    try:
                        Server = ctx.guild.name
                    except:
                        Server = None
                    try:
                        Channel = ctx.channel.name
                    except:
                        Channel = None

                    erembed = discord.Embed(
                        title="\u200b\nEin Fehler ist aufgetreten!\n\u200b",
                        colour=discord.Colour(Utils.Farbe.Red),
                        description=f"**Ausgeführt von:**\n`{ctx.author} | {ctx.author.id}`\n\n"
                                    f"**Command Information:**\n"
                                    f"Executed on Server: `{Server}`\n"
                                    f"Executed in Channel: `{Channel}`\n"
                                    f"Cog: `{ctx.cog}`\n"
                                    f"Command: `{self.client.command_prefix}{ctx.command.name} {ctx.command.signature}`\n"
                                    f"_Executed:_ `{ctx.message.content}`\n\n"
                                    f"**Error:**\n"
                                    f"`{error}`\n\n"
                                    f"**Analytics:**\n"
                                    f"CPU: `{psutil.cpu_percent(interval=1, percpu=True)}`\n"
                                    f"RAM: `{psutil.virtual_memory().percent}`\n\n"
                                    f"**Traceback:**```py\n{str(traceback_text)}\n```",
                        timestamp=datetime.utcnow()
                    )
                    embed.set_footer(text='\u200b', icon_url=Utils.YAML.GET("Bilder", "Clock"))


                    await webhook.send(username="System Benachrichtigung", avatar_url=self.client.user.avatar_url, embed=erembed)

                    await Utils.Messaging.Universal_send(ctx, embed, 15)

        else:

            embed = discord.Embed(
                title='ACHTUNG!',
                colour=discord.Colour(Utils.Farbe.Red),
                description='In diesem Command ist ein schwerwiegender Fehler aufgetreten!\nIch habe die Fehlermeldung and das Developement Team weitergeleitet.'
                            'Tritt dieser Fehler in den nächsten Tagen erneut auf, '
                            'kontaktiere **dringend** den Support: **!s**'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            async with aiohttp.ClientSession() as session:
                url = Utils.YAML.GET("Variables", "ClientSide", "Webhooks", "System")

                webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

                trace = traceback.format_exception(None, error, error.__traceback__)
                if '\nThe above exception was the direct cause of the following exception:\n\n' in trace:
                    trace = trace[
                            :trace.index('\nThe above exception was the direct cause of the following exception:\n\n')]
                    traceback_text = "\n".join(trace)
                else:
                    traceback_text = trace

                y = 0
                for obj in traceback_text:
                    y += len(obj)


                while y >= 2045:
                    traceback_text = traceback_text[:1]
                    y = 0
                    for obj in traceback_text:
                        y += len(obj)

                try:
                    Server = ctx.guild.name
                except:
                    Server = None
                try:
                    Channel = ctx.channel.name
                except:
                    Channel = None

                erembed = discord.Embed(
                    title="\u200b\nEin Fehler ist aufgetreten!\n\u200b",
                    colour=discord.Colour(Utils.Farbe.Red),
                    description=f"**Ausgeführt von:**\n`{ctx.author} | {ctx.author.id}`\n\n"
                                f"**Command Information:**\n"
                                f"Executed on Server: `{Server}`\n"
                                f"Executed in Channel: `{Channel}`\n"
                                f"Cog: `{ctx.cog}`\n"
                                f"Command: `{self.client.command_prefix}{ctx.command.name} {ctx.command.signature}`\n"
                                f"_Executed:_ `{ctx.message.content}`\n\n"
                                f"**Error:**\n"
                                f"`{error}`\n\n"
                                f"**Analytics:**\n"
                                f"CPU: `{psutil.cpu_percent(interval=1, percpu=True)}`\n"
                                f"RAM: `{psutil.virtual_memory().percent}`\n\n"
                                f"**Traceback:**```py\n{str(traceback_text)}\n```",
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text='\u200b', icon_url=Utils.YAML.GET("Bilder", "Clock"))

                await webhook.send(username="System Benachrichtigung", avatar_url=self.client.user.avatar_url,
                                   embed=erembed)

                await Utils.Messaging.Universal_send(ctx, embed, 15)


    # COMMAND_HANDLER


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
