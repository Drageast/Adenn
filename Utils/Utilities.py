import functools
import inspect
import yaml
import sys
import time
import asyncio
from .ErrorHandler import YAMLError


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



class SMOOTH:

    @staticmethod
    async def Embed_ctx(ctx, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await ctx.message.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(seconds_)
            await m.delete()
        except:
            pass

    @staticmethod
    async def Embed_message(message, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await message.delete()
        except:
            pass
            m = await message.channel.send(embed=embed)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass

    @staticmethod
    async def Embed_edit(m, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await m.edit(embed=embed)
            try:
                await m.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds_)
            await m.delete()
        except:
            pass

    @staticmethod
    async def s_file(ctx, file, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await ctx.message.delete()
        except:
            pass
        m = await ctx.send(file=file)
        await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass

    @staticmethod
    async def sm_ctx(ctx, message, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await ctx.message.delete()
        except:
            pass
            m = await ctx.send(message)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass

    @staticmethod
    async def sm_message(message, message_content, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await message.delete()
        except:
            pass
            m = await message.channel.send(message_content)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass


class Pagination:
    def __init__(self, client):
        self.client = client

    async def Pag(self, ctx, content, info = None):

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
