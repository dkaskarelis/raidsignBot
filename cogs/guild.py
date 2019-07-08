import discord
import asyncio
import asyncpg

from discord.ext import commands
from utils.permissions import default_role_perms_comp_raid, bot_perms
from utils.globalfunctions import get_comp_channel_id, get_raid_channel_id


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def compchannel(self, guild_id, channel_id):
        await self.bot.db.execute('''
        UPDATE guild
        SET compchannel = $1
        WHERE id = $2''', channel_id, guild_id)

    async def raidchannel(self, guild_id, channel_id):
        await self.bot.db.execute('''
        UPDATE guild
        SET raidchannel = $1
        WHERE id = $2''', channel_id, guild_id)

    async def category(self, guild_id, category_id):
        await self.bot.db.execute('''
        UPDATE guild
        SET category = $1
        WHERE id = $2''', category_id, guild_id)

    @commands.command()
    async def addraidchannel(self, ctx):
        guild = ctx.guild
        guild_id = guild.id

        category = discord.utils.get(guild.categories, name='Raidsign')

        print(category.id)

        exists = await get_raid_channel_id(self.bot.db, guild_id)

        if exists is not None:
            return

        overwrites_raids_comps = {guild.default_role: default_role_perms_comp_raid,
                                  guild.me: bot_perms}

        raid_channel = await guild.create_text_channel('Comps', overwrites=overwrites_raids_comps)

        await self.raidchannel(guild_id, raid_channel.id)

    @commands.command()
    async def addcompchannel(self, ctx):
        guild = ctx.guild
        guild_id = guild.id

        exists = await get_comp_channel_id(self.bot.db, guild_id)

        print(exists)

        if exists is not None:
            return

        overwrites_raids_comps = {guild.default_role: default_role_perms_comp_raid,
                                  guild.me: bot_perms}

        comp_channel = await guild.create_text_channel('Comps', overwrites=overwrites_raids_comps)

        await self.compchannel(guild_id, comp_channel.id)


def setup(bot):
    bot.add_cog(Guild(bot))