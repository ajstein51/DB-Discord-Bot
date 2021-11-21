########################################################################################################
# AJ Stein
# discord bot itself, will get cmds and send them to the cmd.py 
# CS 4620 Database
########################################################################################################
# imports
import os # for the token 
import discord # pip install -U discord.py
from discord.ext import commands
from dotenv import load_dotenv # $ pip install -U python-dotenv
import random
import cmd

# making an instance of the bot and setting prefix
client = commands.Bot(command_prefix='!')
client.remove_command('help')

# telling us the bot is online
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  cmd.create_connection('game.db')
# end of function  

# help command
@client.command(pass_context=True)
async def help(ctx):
  # color of the left bar
  embed = discord.Embed(
    colour = discord.Colour.dark_teal()
  )
  # contents of the embed
  embed.set_author(name='Commands:')
  embed.add_field(name='Command: !game \'[game name]\' [optional console]', value='Returns: title, console, genre, publisher\nMore Info: Without specifying a console itll return the first one it sees. Game must be wrapped with \'\' and lowercase. This command is for search specific games that you know is formatted correctly, if you are unsure of the format of the game name or would rather have partial matches see !matchsearchgame.', inline=False)
  
  # send a message about cmds
  await ctx.send(embed=embed)
# end of help

########################################################################################################
# Commands
# !game [game_name][opt console] -> details about the game, like: title, console, genre, publisher
@client.command()
async def game(ctx, *args):
  # check if we got args
  if args:
    output = cmd.get_game(args)
    # if len(output) == 0:
    #       await ctx.send("")
    # await ctx.send("Title: "+output[0]+", Console: "+output[1]+", Genre: "+output[2]+", Publisher: "+output[3])
  else:
    await ctx.send("Missing game name")
# end of game cmd


########################################################################################################
# get discord token
load_dotenv()
client.run(os.getenv('TOKEN'))

# To do list in order:
# !game [game_name][opt console] -> details about the game, like: title, console, genre, publisher
# !extendedgame [game_name] -> title, console, genre, publisher, developer, release date, last update
# !allgames [keyword] -> all game titles that match that keyword
# !sales [game_name] -> sale info of the game
# !coverart [game] -> coverart of the game
# !moreinfo [game] -> link the wiki  of the game
# !devsearch [keyword] -> games by a dev
# !publishersearch [keyword] -> games by the publisher
# !matchsearchgame [game] -> match part of the game name to games
# !matchsearchpublisher
# !matchsearchdeveloper
# !releasedatesearch [date1][date2] -> games between those dates
# !lastupdatedatesearch [date1][date2] -> games between those dates
# !topscore [optional num] -> games above this number, otherwise just the top games
# !bottomscore [opt num] -> bottom games below this num or just bottom gamees
# !salessearch [game][optional region] -> give total number unless opt region isnt null
# graph of top sold games by publisher
# graph of top sold games by console
# graph of top sold games by genre

# Ideas for the bot
# get score on game (top/bottom X amount)
# get amount sold of game, if there is diff consoles get indiv of it
# get an image of the game
# get basic info of game, title, console, genre, publisher, 
#   when it was released
# trailer of game from YT?
# top X amount, bottom X amount
# games from X publisher/console/genre
# games from X date to Y date


# client pgad6p3v3f517jp9jzpsz0o4updgmz

# https://id.twitch.tv/oauth2/token?client_id=pgad6p3v3f517jp9jzpsz0o4updgmz&client_secret=p3s2znymqxr05rvw5zjp9bw3m8cruv&grant_type=client_credentials

# {
#     "access_token": "v9o0482wo7vnio559gcta1fgj11htt",
#     "expires_in": 5080720,
#     "token_type": "bearer"
# }

# Pull art from the wiki and add a source to the wiki
# //upload.wikimedia.org/wikipedia/en/thumb/2/2a/Assassin%27s_Creed_Logo.svg/250px-Assassin%27s_Creed_Logo.svg.png	
# game summary from the wiki?
