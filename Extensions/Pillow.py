# Import
import os
from io import BytesIO
import discord
from PIL import Image, ImageDraw, ImageOps, ImageFont
from colorthief import ColorThief
from discord.ext import commands

# Utils
import Utils


# Cog Initialising


class PILLOW(commands.Cog):

    def __init__(self, client):
        self.client = client


    # RANK


    @staticmethod
    def member_check(member, ctx):

        if member is None:
            return ctx.author

        else:
            return member


    @commands.command(aliases=["r"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rank(self, ctx, member: discord.Member = None):

        user = self.member_check(member, ctx)

        data = await Utils.Uccounts.check_Uccount(self, ctx, ctx.author.id, 2)

        async with ctx.typing():
            # LEVEL_ERMITTLUNG

            lvl = 0
            rank = 0
            xp = data.xp
            while True:
                if xp < ((5 * (lvl ** 2)) + (5 * (lvl - 1))):
                    break
                lvl += 1
            xp -= ((5 * ((lvl - 1) ** 2)) + (5 * (lvl - 1)))
            boxes = int((xp / (200 * ((1 / 2) * lvl))) * 200)

            # USER_AVATAR
            asset = user.avatar_url_as(size=512)

            data2 = BytesIO(await asset.read())

            # PREDICTING_DOMINANT_COLOUR
            color_thief = ColorThief(data2)
            color_raw1 = color_thief.get_palette(quality=1)
            color_raw2 = color_thief.get_palette(quality=2)

            color_raw1 = max(color_raw1)
            color_raw2 = max(color_raw2)

            color_raw3 = [color_raw1, color_raw2]

            color = max(color_raw3)

            # IMAGE_PROCESSING
            av = Image.open(data2)
            av = av.resize((445, 445))

            # AVATAR_MASK
            bigsize = (av.size[0] * 3, av.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=512)
            mask = mask.resize(av.size, Image.ANTIALIAS)
            av.putalpha(mask)

            output = ImageOps.fit(av, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save('Utils/Images/output.png')

            # TEXT
            ranking = Image.open('Utils/Images/Ranking_card.jpg')
            draw = ImageDraw.Draw(ranking)
            font = ImageFont.truetype("Utils/Discord_font.ttf", 85)
            draw.text((645, 155), f"| {user.name} | XP: {xp}/{int(200 * ((1 / 2) * lvl))} | Lvl: {lvl} |",
                      color, font=font)
            ranking.paste(av, (45, 45), av)

            # XP_BAR
            x, y, diam = ((boxes * 9) + 166), 565, 103
            draw.ellipse([x, y, x + diam, y + diam], fill=color)
            ImageDraw.floodfill(ranking, xy=(166, 616), value=color, thresh=40)

            # SAVE
            ranking.save('Utils/Images/overlap.png')

            file = discord.File('Utils/Images/overlap.png')

        await Utils.Messaging.Universal_send(ctx, file, 14)
        try:
            os.remove('Utils/Images/overlap.png')
            os.remove('Utils/Images/output.png')
        except:
            pass


# Cog Finishing


def setup(client):
    client.add_cog(PILLOW(client))
