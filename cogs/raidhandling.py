import discord
import asyncio
import asyncpg

from discord.ext import commands
from globalfunctions import selectevent


class Raids(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Alustaa eventin hyllyyn.
    @staticmethod
    async def setupevent(raidname):
        print("XD")

    # Tarkista jos saman niminen event on jo olemassa
    # Ehkä jsoniin lista raideista, joista on jo eventit tehty.
    @commands.command()
    async def addevent(self, ctx, raidname):
        raidname = str(raidname).upper()

    # Tekee evenitin jos sellaista ei ole.
    @commands.command()
    @commands.is_owner()
    async def clearevent(self, ctx, raidname):
        raidname = raidname.upper()
        self.setupevent(raidname)

    @commands.command()
    # @decline.after_invoke
    # @sign.after_invoke
    async def comp(self, ctx, raidname):

        raidname = raidname.upper()

        setup_shelf = selectevent(raidname)
        if setup_shelf is None:
            return

        # channel = bot.get_channel(577485845083324427)

        total_signs = 0

        for key in setup_shelf:
            total_signs += len(setup_shelf[key])

        embed = discord.Embed(
            title='Attending (' + str(total_signs) + ")",
            colour=discord.Colour.blue()
        )

        for key in setup_shelf:
            header = key + " (" + str(len(setup_shelf[key])) + ")"

            class_string = ""
            for nickname in setup_shelf[key]:
                class_string += nickname + "\n"

            if not class_string:
                class_string = "-"

            embed.add_field(name=header, value=class_string, inline=False)

        await ctx.send(embed=embed)

        setup_shelf.close()


def setup(bot):
    bot.add_cog(Raids(bot))
