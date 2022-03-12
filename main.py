from asyncio.windows_events import NULL
import DBManager
from decouple import config
import discord 
from discord.ext import commands

APPID = config('APPID', default='')
TOKEN = config('TOKEN', default='')
CHANNEL_ID = config('CHANNEL_ID', default='')

url = "https://discord.com/api/v8/applications/"+ APPID + "/commands"

bot = commands.Bot(command_prefix='!' , case_insensitive=True)

players = dict()
global updated 
updated = False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord!')


@bot.command(name='leader')
async def leader(ctx):
    msg = "TEST"
    await ctx.send(msg)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    channel = bot.get_channel(int(CHANNEL_ID))
    channel_name = "daily-wordle"
    channel_chk = discord.utils.get(ctx.guild.channels, name=channel_name)
    channel_chk = str(channel_chk.id)
    if channel_chk != CHANNEL_ID:
        msg = "Error: This command is not allowed in this channel"
        await ctx.send(msg)
        return
    
    messages = await channel.history(limit=None).flatten()
   
    numOfGames = parseMsgs(messages, players)

    update_table()
    global updated
    updated = True
    await sendLeaderBoard(ctx, players, channel, numOfGames)
    


#--------------------------------------------------------------------------------------------------------------#

def parseMsgs(messages, players):
    players.clear()
    numOfGames = dict()
    scores = dict()
    game = 0
    for msg in messages:
        if "Wordle" in msg.content:           
            global scr
            scr = score(msg.content.partition('\n')[0].split(' ')[2])
            player = msg.author.name

            if player not in players:
                players[player] = scr
                numOfGames[player] = 1
            
            else:
                current_score = players[player]
                new_score = current_score + scr
                players[player] = new_score
                numOfGames[player] = numOfGames[player] + 1
       
    for player in players.keys():
        players[player] = players[player]/numOfGames[player]
    
    return numOfGames


def score(scr):
    global score2
    match scr:
    
        case "X/6":
           score2 = 7
        
        case "1/6":
            score2 = 1

        case "2/6":
            score2 = 2

        case "3/6":
            score2 = 3

        case "4/6":
            score2 = 4

        case "5/6":
            score2 = 5

        case "6/6":
            score2 = 6

    return score2


def update_table():
    dbManager = DBManager.DBManager()
    if dbManager.tableExists() is False:
        dbManager.createTable()
        dbManager.update(players)
    else:
        dbManager.update(players)

async def sendLeaderBoard(ctx, players, channel, numOfGames):
    embed = discord.Embed(
        title = "Wordle Leaderboard")
    i = 0
    sortList = sorted(players.items(), key=lambda x:x[1])
    players = dict(sortList)
    for player in players:
        i = i + 1
        embed.add_field(name = "Rank " + str(i) + "           Score", value = player + """᲼᲼᲼᲼""" + str(players[player])[0:3], inline = False) 



    await ctx.send(embed=embed)

bot.run(TOKEN)

