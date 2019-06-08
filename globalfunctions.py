

player_classes = ["Warrior", "Rogue", "Hunter", "Warlock", "Mage", "Priest",
                  "Shaman", "Druid", "Declined"]


async def is_valid_class(name):
    name = name.title()

    if name in player_classes:
        return name
    else:
        return None


async def getlevel(db, playerid):
    playerid = int(playerid)

    row = await db.fetchrow('''
    SELECT player.level
    FROM player
    WHERE player.id = $1''', playerid)

    return row


async def getraidid(db, guild_id, raidname):
    row = await db.fetchrow('''
    SELECT raid.id
    FROM raid
    WHERE guildid = $1 AND name = $2 ''', guild_id, raidname)

    return row


async def getuserid(members, name):
    for member in members:
        member_name = member.name + "#" + member.discriminator
        if member_name == name:
            return member.id

    return -1


async def getplayerclass(db, guild_id, player_id):
    print("XD")
    print(guild_id)
    print(player_id)

    row = await db.fetchrow('''
    SELECT class
    FROM membership
    WHERE guildid = $1 AND playerid = $2''', guild_id, player_id)

    print(row)



    if row is None or row['class'] is None:
        return None

    else:
        return row['class']
