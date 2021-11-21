########################################################################################################
# AJ Stein
# this file will do the functions for the cmds
# CS 4620 Database
########################################################################################################
# includes
import sqlite3
from sqlite3 import Error
import math
import os.path
########################################################################################################
# connect to the db
def create_connection(db_file):
    global dbcon
    dbcon = None
    try:
        # something with pathing to fix getting a db connection found from stackoverflow
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dbpath = os.path.join(BASE_DIR, "game.db")
        dbcon = sqlite3.connect(dbpath)
        
        # return dbcon
    except Error as e:
        print(e)
    
# end of fun
########################################################################################################
# Commands
def get_game(args):
    # get the game name or console
    game = ''
    console = ''
    
    # getting the start and end
    start, end = False, False
    
    # counter for getting the console if given
    counter = 0
    
    # parse the args
    if len(args) == 1:
        game = args[0]
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: # get the slice at the start so we dont get a '
                    # game += args[0][1:]
                    game += args[0]
                    game += ' ' 
                    start = True
                    counter += 1
                elif start == True and args[i].find('\'') != -1: # found the end
                    # game += args[i][:-1]
                    game += args[i]
                    counter += 1
                    end = True
                elif start == True and args[i].find('\'') == -1 and end == False: # middle
                    game += args[i]
                    game += ' ' # need a space
                    counter += 1
    # end of else
    # check for console
    if counter < len(args):
        console = args[len(args) - 1]

    console = '\'' + console + '\''
    print(game, "a")

    # get database cur
    cur = dbcon.cursor()
    
    # do the sql query
    if len(console) == 0:
        game = game[1:-1]
        cur.execute("""SELECT title, console, genre, publisher FROM games WHERE title='%s'""" % (game,) )
    else:
        # we got a console
        cur.execute("""SELECT title, console, genre, publisher FROM games WHERE title=%s AND console=%s""" % (game, console) )
    
    # get the query results
    retstring = cur.fetchone()
    print(retstring)
    # close cur
    cur.close()
    # return string
    return retstring
# end of function