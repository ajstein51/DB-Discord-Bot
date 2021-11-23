########################################################################################################
# AJ Stein
# discord bot itself, will get cmds and send them to the cmd.py 
# CS 4620 Database
########################################################################################################
# imports
import os # for the token 
import discord
from discord import colour # pip install -U discord.py
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
  embed = discord.Embed(colour = discord.Colour.dark_teal())
  # contents of the embed
  embed.set_author(name='Commands:')
  embed.add_field(name='!game \'[game name]\' [optional console]', value='Returns: title, console, genre, total sold\nMore Info: Without specifying a console itll return the first one it sees. Game must be wrapped with \' \'. This command is for search specific games that you know is formatted correctly, if you are unsure of the format of the game name or would rather have partial matches see !searchgames.', inline=False)
  embed.add_field(name='!extendedgame \'[game name]\' [optional console]', value='Returns: title, console, genre, publisher, developer, total sold, release date, critic score\nMore Info: Without specifying a console itll return the first one it sees. Game must be wrapped with \' \'. This command is for search specific games that you know is formatted correctly, if you are unsure of the format of the game name or would rather have partial matches see !matchsearchgame.', inline=False)
  embed.add_field(name='!searchgames \'[keywords]\'', value='Returns: title, console, genre, total sold of all games matched\nMore Info: Game must be wrapped with \' \'. Beware of spam this will match all results. If over 12 results found, it will print out 12 random games.', inline=False)
  embed.add_field(name='!searchpublishers \'[publisher]\'', value='Returns: title, console, genre, total sold\nMore Info: Will give 12 games from a publisher that matches your keyword, if more than 12 appear it will pick 12 random. Game must be wrapped with \' \'.', inline=False)
  embed.add_field(name='!searchdeveloper \'[developer]\'', value='Returns: title, console, genre, total sold\nMore Info: Will give 12 games from a developer that matches your keyword, if more than 12 appear it will pick 12 random. Game must be wrapped with \' \'.', inline=False)
  embed.add_field(name='!sales \'[game]\' [optional console]', value='Returns total shipped, total sales, na sales, japan sales, pal sales, other sales')
  embed.add_field(name='!coverart \'[game]\' [optional console]', value='Returns title, console, cover art image\nMore Info: Game must be wrapped with \' \'')
  embed.add_field(name='!randomgame', value='Returns: title, console, genre, publisher, total sales, wiki link, cover art, critic score\nMore Info: Game must be wrapped with \' \'')
  # footer
  embed.set_footer(text="Disclaimer: results of 'unknown', -1, or empty cover art's may appear as the information isnt available.")
  
  # send a message about cmds
  await ctx.send(embed=embed)
# end of help
########################################################################################################
# Commands
# !game [game_name][opt console] -> details about the game, like: title, console, genre, total sold
@client.command()
async def game(ctx, *args):
  # check if we got args
  if args:
    output = cmd.get_game(args)
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name="Game Information")
    if output:
      if output[3] == -1:
        embed.add_field(name=output[0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[1], output[2], output[4]))
      else:
        embed.add_field(name=output[0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[1], output[2], output[3]))
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of game cmd

# !extendedgame [game_name] -> title, console, genre, publisher, developer, total sold, release date, last update
@client.command()
async def extendedgame(ctx, *args):
  # check if we got args
  if args:
    output = cmd.get_extendedgame(args)
    embed = discord.Embed(colour = discord.Colour.dark_blue())
    embed.set_author(name="Extended Game Information")
    if output:
      if output[5] == -1:
        embed.add_field(name=output[0], value="Console: {0}\nGenre: {1}\nPublisher: {2}\nDeveloper: {3}\nTotal Sold Copys Per Console: {4} million\nRelease Date: {5}\nCritic Score: {6}".format(output[1],output[2],output[3],output[4],output[6],output[7],output[8]))
      else:
        embed.add_field(name=output[0], value="Console: {0}\nGenre: {1}\nPublisher: {2}\nDeveloper: {3}\nTotal Sold Copys Per Console: {4} million\nRelease Date: {5}\nCritic Score: {6}".format(output[1],output[2],output[3],output[4],output[5],output[7],output[8]))
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of extendedgame function

# !searchgames [keyword] -> all game titles that match that keyword
@client.command()
async def searchgames(ctx, *args):
  if args:
    output = cmd.get_searchgames(args)  
    # loop through the possible games and add it to be outputted
    embed = discord.Embed(colour = discord.Colour.dark_red())
    embed.set_author(name="Match Results")
    if output:
      for i in range(len(output)):
        if output[3] == -1:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[i][1], output[i][2], output[i][4]))
        else:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[i][1], output[i][2], output[i][3]))

      # send message
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of searchgames function

# !searchpublishers [keyword] -> 10 random games from publishers that match that keyword
@client.command()
async def searchpublishers(ctx, *args):
  if args:
    output = cmd.get_searchpublisher(args)  
    # loop through the possible games and add it to be outputted
    embed = discord.Embed(colour = discord.Colour.magenta())
    embed.set_author(name="Match Results")
    if output: # if output isnt empty
      for i in range(len(output)):
        if output[3] == -1:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nPublisher: {3}".format(output[i][1], output[i][2], output[i][4], output[0][5]))
        else:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nPublisher: {3}".format(output[i][1], output[i][2], output[i][3], output[0][5]))

      # send message
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of searchpublishers function

# !searchdevelopers [keyword] -> all developers titles that match that keyword, 10 random games
@client.command()
async def searchdevelopers(ctx, *args):
  if args:
    output = cmd.get_searchpublisher(args)  
    # loop through the possible games and add it to be outputted
    embed = discord.Embed(colour = discord.Colour.dark_magenta())
    embed.set_author(name="Match Results")
    if output:
      for i in range(len(output)):
        if output[3] == -1:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nDeveloper: {3}".format(output[i][1], output[i][2], output[i][4], output[0][5]))
        else:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nDeveloper: {3}".format(output[i][1], output[i][2], output[i][3], output[0][5]))

      # send message
      await ctx.send(embed=embed)
    else: #output empty
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of searchdevelopers function

# !sales [game_name] [option console] -> all sale info of the game
@client.command()
async def sales(ctx, *args):
  # check if we got args
  if args:
    output = cmd.get_sales(args)
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name="Sales Information")
    if output:
      embed.add_field(name=output[0],  value="Console: {0}\nTotal Shipped: {1} million\nTotal Sold: {2} million\nNA Sales: {3} million\nJP Sales: {4} million\nPAL Sales: {5} million\nOther Sales: {6} million".format(output[1], output[2], output[3], output[4], output[5], output[6], output[7]))
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of sales function

# !coverart [game] -> coverart of the game
@client.command()
async def coverart(ctx, *args):
  if args:
    output = cmd.get_coverart(args)    
    embed = discord.Embed(colour = discord.Colour.dark_gold())
    embed.set_author(name="Cover Art")
    if output:
          embed.add_field(name=output[0], value='Console: {0}'.format(output[1]))
          embed.set_image(url='https://{0}'.format(output[2]))
          await ctx.send(embed=embed)
    else: 
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing game name")
# end of coverart

# !randomgame -> give a random game and its info, title, console, genre, publisher, total sold/shipped, wiki, cover art, score
@client.command()
async def randomgame(ctx):
  output = cmd.get_randomgame()    
  embed = discord.Embed(colour = discord.Colour.dark_theme())
  embed.set_author(name="Random Game")
  if output:
        # embed.add_field(name=output[0], value='Console: {0}'.format(output[1]))
        # embed.set_image(url='https://{0}'.format(output[2]))
        # await ctx.send(embed=embed)
  else: 
    await ctx.send("No matches found")
# end of randomgame function
########################################################################################################
# get discord token
load_dotenv()
client.run(os.getenv('TOKEN'))

# To do list in order:
# !game [game_name][opt console] -> details about the game, like: title, console, genre, publisher | CHECK
# !extendedgame [game_name] -> title, console, genre, publisher, developer, release date, last update | CHECK
# !searchgames [keyword] -> all game titles that match that keyword | CHECK
# !searchpublishers [keyword] -> all publishers titles that match that keyword, 10 random games | CHECK
# !searchdevelopers [keyword] -> all developers titles that match that keyword, 10 random games | CHECK
# !sales [game_name] -> all sale info of the game | CHECK
# !coverart [game] -> coverart of the game | CHECK
# !randomgame -> give a random game and its info, title, genre, publisher, total sold/shipped, wiki, cover art, score
# !moreinfo [game] -> link the wiki  of the game
# !searchdev [keyword] -> games by a dev
# !searchpublisher [keyword] -> games by the publisher
# !releasedatesearch [date1][date2] -> games between those dates
# !lastupdatedatesearch [date1][date2] -> games between those dates
# !topscore [optional num] -> games above this number, otherwise just the top games
# !bottomscore [opt num] -> bottom games below this num or just bottom gamees
# !salessearch [number][optional region] -> give total number above x num unless opt region isnt null
# graph of top sold games by publisher
# graph of top sold games by console
# graph of top sold games by genre
