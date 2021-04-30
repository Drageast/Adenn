import functools
import inspect
import yaml
import sys
import time
import asyncio
from .ErrorHandler import YAMLError
import discord
from discord.ext import commands


class Object(object):
    pass


class Wrappers:

    @staticmethod
    def TimeLogger(func):

        def wrapper_NONE_async(*args, **kwargs):
            before = time.time()
            func_ = func(*args, **kwargs)
            print(f"Executed Function: |{func.__name__}|-|NONE_ASYNC| ; Execution took: |{time.time() - before} seconds|")
            return func_

        @functools.wraps(func)
        async def wrapper_IS_async(*args, **kwargs):
            before = time.time()
            func_ = await func(*args, **kwargs)
            print(f"Executed Function: |{func.__name__}|-|IS_ASYNC| ; Execution took: |{time.time() - before} seconds|")
            return func_

        if inspect.iscoroutinefunction(func):
            return wrapper_IS_async
        else:
            return wrapper_NONE_async


class Checker:

    @staticmethod
    @Wrappers.TimeLogger
    def LATENCY(client):
        before = time.time()
        client.ticket.insert_one({"_id": 1})
        after = time.time() - before
        client.ticket.delete_one({"_id": 1})

        return after


class YAML:

    @staticmethod
    @Wrappers.TimeLogger
    def PATH(container: str):
        try:
            with open("Utils/config.yaml", "r") as f:
                container_ = yaml.safe_load(f)
            container_ = container_[container]
            return container_
        except Exception as e:
            raise YAMLError(e)

    @staticmethod
    @Wrappers.TimeLogger
    def GET(Container: str, *Load: str):
        try:
            dict_ = YAML.PATH(Container)
            new_dict = dict_
            for load in Load:
                new_dict = new_dict[load]

            return new_dict
        except Exception as e:
            raise YAMLError(e)

    @staticmethod
    @Wrappers.TimeLogger
    def TOKEN(password: int):
        password_ = password**4

        if password_ == YAML.GET("Variables", "ClientSide", "Password"):

            return YAML.GET("Variables", "ClientSide", "Token")

        else:
            sys.exit(EnvironmentError("Das Passwort ist Falsch!"))


class Messaging:


    @staticmethod
    async def Universal_send(context: [commands.Context, discord.Message], obj: [discord.Embed, discord.File, str], seconds: float = 8):

        # Embed Check
        if isinstance(obj, discord.Embed):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(embed=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(embed=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        # Nachricht Check
        elif isinstance(obj, str):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        # Datei Check
        elif isinstance(obj, discord.File):

            if isinstance(context, commands.Context):

                try:
                    await context.message.delete()
                except:
                    pass
                try:
                    m = await context.send(file=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            elif isinstance(context, discord.Message):

                try:
                    await context.delete()
                except:
                    pass
                try:
                    m = await context.channel.send(file=obj)
                except:
                    return
                await asyncio.sleep(seconds)
                try:
                    await m.delete()
                except:
                    return

            else:
                raise AttributeError("Context ist nicht: [commands.Context, discord.Message]")

        else:
            raise AttributeError("Objekt ist nicht: [discord.Embed, discord.File, str]")


    @staticmethod
    async def Universal_edit(message_obj, obj: [discord.Embed, discord.File, str], seconds: float = 8):

        # Embed Check
        if isinstance(obj, discord.Embed):

            try:
                await message_obj.edit(embed=obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        # Datei Check
        elif isinstance(obj, discord.File):

            try:
                await message_obj.edit(file=obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        # Nachricht Check
        elif isinstance(obj, str):

            try:
                await message_obj.edit(obj)
            except:
                return
            try:
                await message_obj.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds)
            try:
                await message_obj.delete()
            except:
                return

        else:

            raise AttributeError(f"Objekt ist nicht: [discord.Embed, discord.File, str] => {type(obj)}")


    @staticmethod
    async def Paginator(self, ctx, content: list, info: str = None):

        contents = content

        info_ = None

        pages = len(contents)

        cur_page = 0
        try:
            await ctx.message.delete()
        except:
            pass

        message = await ctx.send(embed=contents[cur_page])

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("⏹️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        if info is not None:
            await message.add_reaction("ℹ️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⏪", "◀️", "⏹️", "▶️", "⏩", "ℹ️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

                if str(reaction.emoji) == "▶️":
                    if cur_page != pages - 1:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page])
                        await message.remove_reaction(reaction, user)
                    else:
                        pass

                elif str(reaction.emoji) == "◀️" and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    try:
                        await message.delete()
                    except:
                        pass
                    try:
                        await info_.delete()
                    except:
                        pass
                    break

                elif str(reaction.emoji) == "⏪":
                    cur_page = 0
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏩":
                    cur_page = pages - 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "ℹ️":
                    if info_ is None:
                        info_ = await ctx.send(info)
                    else:
                        try:
                            await info_.delete()
                        except:
                            pass
                        info_ = None

                    await message.remove_reaction(reaction, user)


                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except:
                    pass
                try:
                    await info_.delete()
                except:
                    pass
                break


class Permissions:

    @staticmethod
    def Ban_perm():
        async def peridicate1(ctx):
            return ctx.author.guild_permissions.ban_members

        return commands.check(peridicate1)

    @staticmethod
    def Clear_perm():
        async def peridicate4(ctx):
            return ctx.author.guild_permissions.manage_messages

        return commands.check(peridicate4)

    @staticmethod
    def Lock_Unlock_perm():
        async def peridicate3(ctx):
            return ctx.author.guild_permissions.manage_channels \
                   and ctx.author.guild_permissions.manage_guild

        return commands.check(peridicate3)

    @staticmethod
    def Kick_perm():
        async def peridicate2(ctx):
            return ctx.author.guild_permissions.kick_members

        return commands.check(peridicate2)


# GET_CHANNEL


async def get_channel(user, embed, name):
    channel = discord.utils.get(user.guild.text_channels, name=name)

    if channel is None:
        return

    else:

        await channel.send(embed=embed)
        return


class Farbe:

    Dp_Red = 0xc23b22

    Dp_Blue = 0x779ecb

    Dp_Green = 0xa2d0c0

    Lp_Green = 0x78e08f

    Lp_Blue = 0xadd8e6

    Lp_Red = 0xff3328

    Red = 0xff0000

    Orange = 0xfd9644

    Darker_Theme = 0x23272a

    ShimariRosa = 0xff00ff
