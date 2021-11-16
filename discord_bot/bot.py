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
import cmd

# making an instance of the bot
client = discord.Client()

# telling us the bot is online
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
# end of function


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!hi'):
    await message.channel.send("hi")


# get discord token
load_dotenv()
client.run(os.getenv('TOKEN'))

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
