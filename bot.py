import discord
import os
import json
import asyncio
import asyncpg

from discord.ext import commands

''' 
- Bot should respond if given information was invalid or otherwise didn't do anything.
- Note when getting members from guilds, if member leaves it can be an issue
- Make embed with info and post it to bot commands etc
- Make exception for cooldown in testcog
- Test what permissions bot needs
- Make sure getting channel works in all sending methods if its deleted and ID is in DB but not in guild cuz deleted
- change fetch message on most channels to fetch it from the proper channel
- improve autosign_add db wise
- on_ready use executeman
- setup_channels could be combined with the other one that checks all channels to reduce 1 query
- if all comp channels are deleted when bot comes online they are not deleted from db
- if bot is not given permissions it leaves the guild
- add to help like important tags like how to create raid etc and make embeds of those
- on guild_channel_delete could be improved to create the channel back, doesn't need to clear signs right?

- \U0001f1fe YES -- 
- \U0001f1f3 NO -- 
- \U0001f1e6 A -- 
- \U0000267f wheelchair

- TO TEST:
    - clear_guild_from_db
    - setup_channels with on_ready
    
- TESTED:
    - membership
    - guild
    - misc
'''


def get_cfg():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    with open('config.json') as json_data_file:
        cfg = json.load(json_data_file)
    return cfg


async def do_setup(cfg):
    pool = await asyncpg.create_pool(database=cfg["pg_db"], user=cfg["pg_user"], password=cfg["pg_pw"])

    fd = open("setup.sql", "r")
    file = fd.read()
    fd.close()

    # Remove empty values
    sqlcommands = file.split(';')
    sqlcommands = list(filter(None, sqlcommands))

    for command in sqlcommands:
        await pool.execute(command)

    return pool


class RaidSign(commands.Bot):
    def __init__(self, **kwargs):
        self.command_aliases = None

        super().__init__(**kwargs)
        self.remove_command('help')

        # Load cogs
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                name = filename[:-3]
                self.load_extension(f"cogs.{name}")

        self.data()

    def data(self):
        command_aliases = {}
        for command in self.commands:
            if command.aliases:
                command_aliases[command.name] = command.aliases
        self.command_aliases = command_aliases


def run_bot():
    cfg = get_cfg()

    try:
        pool = asyncio.get_event_loop().run_until_complete(do_setup(cfg))
    except Exception as e:
        return

    bot = RaidSign(command_prefix=cfg['prefix'])
    bot.pool = pool
    bot.run(cfg['token'])


run_bot()
