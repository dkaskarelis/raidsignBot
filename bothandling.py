import discord
import os
import json
import asyncio
import asyncpg

'''
- When player is added to raid, should check if playername has changed aka if the user has changed their discord name
  Maybe this can be done with transasctions, insert into table -> if exists -> update user name. 
- Bot should respond if given information was invalid or otherwise didn't do anything.
- Add some way of auto signing to raids
- Raids should tell the day like "Monday" instead of date and maybe time also
- Addevent could make a message and those who react to it get signed up
- Then add a role for those and then iterate over all who have that role in guild
- Command to track attendance and clear raid with one "master" command
- Add guild ID to raid, maybe user and make it primary key
- Add note to raid with " " then get the note with ctx.message.content.split("")
- You can get Message from msg = await ctx.message....
- Make cog creation from list a function, used in levels and raidhandling atleast
- There might be issues if a player is in multiple servers, which use the bot
'''


from discord.ext import commands

os.chdir(os.path.dirname(os.path.realpath(__file__)))
with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)


bot = commands.Bot(command_prefix=cfg["prefix"])
bot.remove_command('help')


async def setup():
    bot.db = await asyncpg.connect(database=cfg["pg_db"], user=cfg["pg_user"], password=cfg["pg_pw"])

    # await bot.db.execute('''DROP TABLE IF EXISTS ''')

    fd = open("setupsql.txt", "r")
    file = fd.read()
    fd.close()

    sqlcommands = file.split(';')
    sqlcommands = list(filter(None, sqlcommands))

    for command in sqlcommands:
        await bot.db.execute(command)


@bot.event
async def on_ready():
    print('Bot is ready.')


# Load all cogs (classes)
for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        name = filename[:-3]
        bot.load_extension(f"cogs.{name}")

asyncio.get_event_loop().run_until_complete(setup())
bot.run(cfg["token"])
