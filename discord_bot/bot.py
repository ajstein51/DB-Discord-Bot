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
import cmd
import re # pip install regex
import matplotlib.pyplot as plt # pip install matplotlib

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
  embed.add_field(name='!searchreleasedate [YYYY-MM-DD] [YYYY-MM-DD]', value='Returns: title, console, genre, total sold, release date\nMore Info: Will give up to 12 games found, if more than 12 games appear it will pick 12 games at random.')
  embed.add_field(name='!searchlastupdate [YYYY-MM-DD] [YYYY-MM-DD]', value='Returns: title, console, genre, total sold, last update\nMore Info: Will give up to 12 games found, if more than 12 games appear it will pick 12 games at random.')
  embed.add_field(name='!sales \'[game]\' [optional console]', value='Returns total shipped, total sales, na sales, japan sales, pal sales, other sales')
  embed.add_field(name='!coverart \'[game]\' [optional console]', value='Returns title, console, cover art image\nMore Info: Game must be wrapped with \' \'')
  embed.add_field(name='!randomgame', value='Returns: title, console, genre, publisher, total sales, wiki link, cover art, critic score\nMore Info: Game must be wrapped with \' \'')
  embed.add_field(name='!topscore', value='Returns: title, console, genre, critic score, total sales\n')
  embed.add_field(name='!bottomscore [optional top value]', value='Returns: title, console, genre, critic score, total sales\nMore Info: The optional number allows you to place the maximum score it can have')
  embed.add_field(name='!genregraph', value='Returns: Pie Graph\nMore Info: Total amount of games per genre.')
  embed.add_field(name='!consolegraph', value='Returns: Pie Graph\nMore Info: Total amount of consoles per game.')
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
    if output != -1:
      if output[3] == -1:
        embed.add_field(name=output[0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[1], output[2], output[4]))
      else:
        embed.add_field(name=output[0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million".format(output[1], output[2], output[3]))
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found, check format or search with !searchgames")
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
    if output != -1:
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
        if output[i][3] == -1:
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
    if output != -1: # if output isnt empty
      for i in range(len(output)):
        if output[i][3] == -1:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nPublisher: {3}".format(output[i][1], output[i][2], output[i][4], output[0][5]))
        else:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nPublisher: {3}".format(output[i][1], output[i][2], output[i][3], output[0][5]))

      # send message
      await ctx.send(embed=embed)
    else:
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing publisher name")
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
        if output[i][3] == -1:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nDeveloper: {3}".format(output[i][1], output[i][2], output[i][4], output[0][5]))
        else:
          embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nDeveloper: {3}".format(output[i][1], output[i][2], output[i][3], output[0][5]))

      # send message
      await ctx.send(embed=embed)
    else: #output empty
      await ctx.send("No matches found")
  else:
    await ctx.send("Missing developer name")
# end of searchdevelopers function

# !releasedatesearch [date1][date2] -> games between those dates
@client.command()
async def searchreleasedate(ctx, *args):
  # check if we got args
  if len(args) == 2:
    # check the regex
    # check that the 2 args in the format: YYYY-MM-DD
    d1 = args[0]
    d2 = args[1]

    # check the regex (format of the user input)
    d1_check = re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", d1)
    d2_check = re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", d2)
    
    # check the bools
    if d1_check and d2_check:
      output = cmd.get_searchreleasedate(args)
      if output:
        embed = discord.Embed(colour = discord.Colour.dark_blue())
        embed.set_author(name="Release Date Search")
        for i in range(len(output)):
          if output[i][3] == -1:
            embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nRelease Date: {3}".format(output[i][1], output[i][2], output[i][4], output[i][5]))
          else:
            embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nRelease Date: {3}".format(output[i][1], output[i][2], output[i][3], output[i][5]))
        # send message
        await ctx.send(embed=embed)
      else:
        await ctx.send("No matches found")
  else:
    await ctx.send("Problem with arguments, check format [YYYY-MM-DD]")
# end of searchreleasedate

# !searchlastupdatedate [date1][date2] -> games between those dates
@client.command()
async def searchlastupdate(ctx, *args):
  # check if we got args
  if len(args) == 2:
    # check the regex
    # check that the 2 args in the format: YYYY-MM-DD
    d1 = args[0]
    d2 = args[1]

    # check the regex (format of the user input)
    d1_check = re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", d1)
    d2_check = re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", d2)
    
    # check the bools
    if d1_check and d2_check:
      output = cmd.get_searchlastupdate(args)
      if output:
        embed = discord.Embed(colour = discord.Colour.dark_teal())
        embed.set_author(name="Last Update Search")
        for i in range(len(output)):
          if output[i][3] == -1:
            embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nLast Update: {3}".format(output[i][1], output[i][2], output[i][4], output[i][5]))
          else:
            embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nLast Update: {3}".format(output[i][1], output[i][2], output[i][3], output[i][5]))
        # send message
        await ctx.send(embed=embed)
      else:
        await ctx.send("No matches found")
  else:
    await ctx.send("Problem with arguments, check format [YYYY-MM-DD]")
# end of searchreleasedate

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
    if output[4] == -1:
      embed.add_field(name=output[0], value='Console: {0}\nGenre: {1}\nPublisher: {2}\nTotal Sold: {3}\nCritic Score: {4}\nWiki Page: {5}'.format(output[1], output[2], output[3], output[5], output[6], output[7]))
      embed.set_image(url='https://{0}'.format(output[7]))
      await ctx.send(embed=embed)
    else:
      embed.add_field(name=output[0], value='Console: {0}\nGenre: {1}\nPublisher: {2}\nTotal Sold: {3}\nCritic Score: {4}\nWiki Page: {5}'.format(output[1], output[2], output[3], output[4], output[6], output[7]))
      embed.set_image(url='https://{0}'.format(output[7]))
      await ctx.send(embed=embed)
    # end of else
  else: 
    await ctx.send("No matches found")
# end of randomgame function

# !topscore [optional num] -> games above this number, otherwise just the top games
@client.command()
async def topscore(ctx):
  output = cmd.get_topscore()    
  embed = discord.Embed(colour = discord.Colour.greyple())
  embed.set_author(name="Top Scores")
  if output:
    for i in range(len(output)):
      if output[i][3] == -1:
        embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nCritic Score: {3}".format(output[i][1], output[i][2], output[i][4], output[i][5]))
      else:
        embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nCritic Score: {3}".format(output[i][1], output[i][2], output[i][3], output[i][5]))
    # send message
    await ctx.send(embed=embed)
# end of topscore cmd title, console, genre, critic score, total sales

# !bottomscore [opt num] -> bottom games below this num or just bottom gamees
@client.command()
async def bottomscore(ctx, *args):
  numcheck = re.match("[0-9]+", args[0])
  if numcheck:
    output = cmd.get_bottomscore(args)
  else:
    output = cmd.get_bettomscore()    
  embed = discord.Embed(colour = discord.Colour.greyple())
  embed.set_author(name="Bottom Scores")
  if output:
    for i in range(len(output)):
      if output[i][3] == -1:
        embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nCritic Score: {3}".format(output[i][1], output[i][2], output[i][4], output[i][5]))
      else:
        embed.add_field(name=output[i][0],  value="Console: {0}\n Genre: {1}\nTotal Sold: {2} million\nCritic Score: {3}".format(output[i][1], output[i][2], output[i][3], output[i][5]))
    # send message
    await ctx.send(embed=embed)
  else:
    await ctx.send("Check args")
# end of bottomscore

# graph of games sold by genre
@client.command()
async def genregraph(ctx):
  output = cmd.get_genregraph()
  # get the names and values
  labels = []
  pointlist = []
  # split the list of pairs
  for i in range(len(output)):
    labels.append(output[i][0])
    pointlist.append(output[i][1])
  # end of i
  
  # swap some values around so output isnt terrible
  def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
  # end of swap function
  
  # swap music and sports
  pointlist = swapPositions(pointlist, 8, 17)
  labels = swapPositions(labels, 8, 17)
  
  # swap board games and puzzle
  pointlist = swapPositions(pointlist, 3, 11)
  labels = swapPositions(labels, 3, 11)
  
  # swap fighting and misc
  pointlist = swapPositions(pointlist, 7, 5)
  labels = swapPositions(labels, 7, 5)
  
  # # swap action-adventure and education
  pointlist = swapPositions(pointlist, 1, 4)
  labels = swapPositions(labels, 1, 4)
  
  # make graph
  plt.pie(pointlist, wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'})
  
  # add % onto the label
  newlabels = [f'{labels[i]} {int(round(pointlist[i]/sum(pointlist)*100))}%' for i in range(len(labels))]
  
  # make legend
  plt.legend(labels=newlabels, loc='center left', bbox_to_anchor=(-.3, .5), fontsize=8)
  
  plt.title('Genre Graph')
  plt.tight_layout()
  plt.savefig('graph.png')
  
  # output
  await ctx.send(file=discord.File('graph.png'))
# end of function

# graph of games sold by console
@client.command()
async def consolegraph(ctx):
  # get output 
  output = cmd.get_consolegraph()
  
  # get the names and values
  labels = []
  pointlist = []
  # split the list of pairs
  for i in range(len(output)):
    if(output[i][1] >= 500):
      labels.append(output[i][0])
      pointlist.append(output[i][1])
  # end of i
  
  # swap some values around so output isnt terrible
  def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
  # end of swap function
  
  # add % onto the label
  newlabels = [f'{labels[i]} {int(round(pointlist[i]/sum(pointlist)*100))}%' for i in range(len(labels))]

  plt.pie(pointlist, labels = newlabels, wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'}, textprops={'size': 'small'}, rotatelabels=True)

  plt.title('Console Graph', loc='left')
  plt.tight_layout()
  plt.savefig('graph.png')
  
  # output
  await ctx.send(file=discord.File('graph.png'))
# end of function

########################################################################################################
# get discord token
load_dotenv()
client.run(os.getenv('TOKEN'))