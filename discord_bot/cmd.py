########################################################################################################
# AJ Stein
# this file will do the functions for the cmds
# CS 4620 Database
# Summary of SQL usage
########################################################################################################
# includes
import sqlite3
from sqlite3 import Error
import random
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
# !game [game_name][opt console] -> details about the game, like: title, console, genre, total sold
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
        counter += 1
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: 
                    game += args[0]
                    game += ' ' 
                    start = True
                    counter += 1
                elif start == True and args[i].find('\'') != -1: # found the end
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

    # get database cur
    cur = dbcon.cursor()

    # do the sql query
    if len(console) == 2: # because console will always have '' in it
        try:
            cur.execute("""SELECT title, console, genre, total_sales, total_shipped FROM games INNER JOIN stats on games.idx = stats.idx WHERE title LIKE %s""" % game)
        except Exception:
            return -1
    else:
        # we got a console
        try:
            cur.execute("""SELECT title, console, genre, total_sales, total_shipped FROM games INNER JOIN stats on games.idx = stats.idx WHERE title LIKE %s AND console LIKE %s""" % (game, console) )
        except Exception:
            return -1
    # get the query results
    retstring = cur.fetchone()

    # close cur
    cur.close()
    # return the list of strings
    return retstring
# end of get_game function
########################################################################################################
# !extendedgame [game_name] -> title, console, genre, publisher, developer, total sold, release date, last update
def get_extendedgame(args):
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
        counter += 1
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: 
                    game += args[0]
                    game += ' ' 
                    start = True
                    counter += 1
                elif start == True and args[i].find('\'') != -1: # found the end
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

    # get database cur
    cur = dbcon.cursor()

    # do the sql query
    if len(console) == 2: # because console will always have '' in it
        try:
            cur.execute("""SELECT title, console, genre, publisher, developer, total_sales, total_shipped, release_date, critic_score FROM games INNER JOIN stats on games.idx = stats.idx WHERE title LIKE %s""" % game)
        except Exception:
            return -1
    else:
        # we got a console
        try:
            cur.execute("""SELECT title, console, genre, publisher, developer, total_sales, total_shipped, release_date, last_update FROM games INNER JOIN stats on games.idx = stats.idx WHERE title=%s AND console=%s""" % (game, console) )
        except Exception:
            return -1
    # get the query results
    retstring = cur.fetchone()

    # close cur
    cur.close()
    # return the list of strings
    return retstring
# end of get_extendedgame function
########################################################################################################
# !searchgames [keyword] -> all game titles that match that keyword
def get_searchgames(args):
    # get the game name or console
    game = ''
    
    # getting the start and end
    start, end = False, False
    
    # parse the args
    if len(args) == 1:
        game = args[0][1:-1]
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: # get the slice at the start so we dont get a '
                    game += args[0][1:]
                    game += ' ' 
                    start = True
                elif start == True and args[i].find('\'') != -1: # found the end
                    game += args[i][:-1]
                    end = True
                elif start == True and args[i].find('\'') == -1 and end == False: # middle
                    game += args[i]
                    game += ' ' # need a space
        # end of for

    # get database cur
    cur = dbcon.cursor()

    # format for the wildcards
    game = '\'%'+game+'%\''

    # do the sql query
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped FROM stats INNER JOIN games ON stats.idx = games.idx WHERE title LIKE %s""" % game)
    
    # get the query results
    allmatch = cur.fetchall()

    # return var 
    retstring = []
    
    # get 10 random results
    if(len(allmatch) > 12):
        store_int = []
        for i in range(12):
            # get random game from the list
            random_game = random.randint(0, len(allmatch) - 1)
            # store the game and make sure we didnt already have it
            if random_game not in store_int:
                store_int.append(random_game)
                retstring.append(allmatch[random_game])
            else:
                # already had it try go again
                i -= 1
    else: # less than 10 games in the list just print them all
        retstring = allmatch

    # close cur
    cur.close()
    # return the list of strings
    return retstring    
# end of get_searchgames function
########################################################################################################
# !searchpublishers [keyword] -> 10 random games from publishers that match that keyword
def get_searchpublisher(args):
    # get the game name or console
    publish = ''
    
    # getting the start and end
    start, end = False, False
    
    # parse the args
    if len(args) == 1:
        publish = args[0][1:-1]
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: # get the slice at the start so we dont get a '
                    publish += args[0][1:]
                    publish += ' ' 
                    start = True
                elif start == True and args[i].find('\'') != -1: # found the end
                    publish += args[i][:-1]
                    end = True
                elif start == True and args[i].find('\'') == -1 and end == False: # middle
                    publish += args[i]
                    publish += ' ' # need a space
    # end of else

    # get database cur
    cur = dbcon.cursor()
    
    # format for the wildcards
    publish = '\'%'+publish+'%\''
    
    # do the sql query, 10 random games from the publisher
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped, publisher FROM stats INNER JOIN games ON stats.idx = games.idx WHERE publisher LIKE %s""" % publish)
    
    # get the query results
    allmatch = cur.fetchall()
   
    # return var 
    retstring = []
    
    # get 10 random results
    if(len(allmatch) > 12):
        store_int = []
        for i in range(12):
            # get random game from the list
            random_game = random.randint(0, len(allmatch) - 1)
            # store the game and make sure we didnt already have it
            if random_game not in store_int:
                store_int.append(random_game)
                retstring.append(allmatch[random_game])
            else:
                # already had it try go again
                i -= 1
    else: # less than 10 games in the list just print them all
        retstring = allmatch
        
    # close cur
    cur.close()
    # return the list of strings
    return retstring  
# end of get_searchpublisher
########################################################################################################
# !searchdevelopers [keyword] -> all developers titles that match that keyword, 10 random games
def get_searchdevelopers(args):
    # get the game name or console
    dev = ''
    
    # getting the start and end
    start, end = False, False
    
    # parse the args
    if len(args) == 1:
        dev = args[0][1:-1]
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: # get the slice at the start so we dont get a '
                    dev += args[0][1:]
                    dev += ' ' 
                    start = True
                elif start == True and args[i].find('\'') != -1: # found the end
                    dev += args[i][:-1]
                    end = True
                elif start == True and args[i].find('\'') == -1 and end == False: # middle
                    dev += args[i]
                    dev += ' ' # need a space
    # end of else

    # get database cur
    cur = dbcon.cursor()
    
    # format for the wildcards
    dev = '\'%'+dev+'%\''
    
    # do the sql query, 10 random games from the publisher
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped, developer FROM stats INNER JOIN games ON stats.idx = games.idx WHERE developer LIKE %s""" % dev)
    
    # get the query results
    allmatch = cur.fetchall()
   
    # return var 
    retstring = []
    
    # get 10 random results
    if(len(allmatch) > 12):
        store_int = []
        for i in range(12):
            # get random game from the list
            random_game = random.randint(0, len(allmatch) - 1)
            # store the game and make sure we didnt already have it
            if random_game not in store_int:
                store_int.append(random_game)
                retstring.append(allmatch[random_game])
            else:
                # already had it try go again
                i -= 1
    else: # less than 10 games in the list just print them all
        retstring = allmatch
        
    # close cur
    cur.close()
    # return the list of strings
    return retstring  
# end of get_searchdevelopers
########################################################################################################
# !sales [game_name] [option console] -> all sale info of the game
def get_sales(args):
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
        counter += 1
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: 
                    game += args[0]
                    game += ' ' 
                    start = True
                    counter += 1
                elif start == True and args[i].find('\'') != -1: # found the end
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

    # get database cur
    cur = dbcon.cursor()

    # do the sql query
    if len(console) == 2: # because console will always have '' in it
        cur.execute("""SELECT title, console, total_shipped, total_sales, na_sales, jp_sales, pal_sales, other_sales FROM games INNER JOIN stats on games.idx = stats.idx WHERE title LIKE %s""" % game)
    else:
        # we got a console
        cur.execute("""SELECT title, console, total_shipped, total_sales, na_sales, jp_sales, pal_sales, other_sales FROM games INNER JOIN stats on games.idx = stats.idx WHERE title LIKE %s AND console LIKE %s""" % (game, console) )
    # get the query results
    retstring = cur.fetchone()

    # close cur
    cur.close()
    # return the list of strings
    return retstring
# end of get_sales
########################################################################################################
# !coverart [game] -> coverart of the game
def get_coverart(args):
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
        counter += 1
    else:
        for i in range(len(args)):
            # never got a ' 
            if args[0].find('\'') == -1:
                return -1
            else:
                # find where it ends and add it to game
                if start == False: 
                    game += args[0]
                    game += ' ' 
                    start = True
                    counter += 1
                elif start == True and args[i].find('\'') != -1: # found the end
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

    # get database cur
    cur = dbcon.cursor()

    # do the sql query
    if len(console) == 2: # because console will always have '' in it
        cur.execute("""SELECT title, console, img FROM wiki INNER JOIN games ON wiki.idx = games.idx WHERE title LIKE %s""" % game)
    else: # we got a console
        cur.execute("""SELECT title, console, img FROM wiki INNER JOIN games ON wiki.idx = games.idx WHERE title LIKE %s AND console LIKE %s""" % (game, console))
    
    # get the query results
    retstring = cur.fetchone()

    # close cur
    cur.close()
    # return the list of strings
    return retstring
# end of get_coverart
########################################################################################################
# !randomgame -> give a random game and its info, title, genre, publisher, total sold/shipped, wiki, cover art, score
def get_randomgame():
    randidx = random.randint(0, 57949) # total tuples
    
    # get database cur
    cur = dbcon.cursor()
    
    # do the query
    cur.execute("""SELECT title, console, genre, publisher, total_sales, total_shipped, critic_score, img FROM games JOIN stats JOIN wiki ON games.idx = stats.idx AND games.idx = wiki.idx WHERE games.idx = {0}""".format(randidx))
    
    # get the query results
    retstring = cur.fetchone()

    # close cur
    cur.close()
    # return the list of strings
    return retstring
# endof get_randomgame
########################################################################################################
# !releasedatesearch [date1][date2] -> games between those dates
def get_searchreleasedate(args):
    d1 = args[0]
    d2 = args[1]
    cur = dbcon.cursor()
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped, release_date FROM games INNER JOIN stats ON games.idx = stats.idx WHERE release_date >= '{0}' AND release_date <= '{1}'""".format(d1, d2))
    allmatch = cur.fetchall()

    # see if there are more than 12 games
    if(len(allmatch) > 12):
        retstring = []
        store_int = []
        for i in range(12):
            random_game = random.randint(0, len(allmatch) - 1)
            if random_game not in store_int:
                store_int.append(random_game)
                retstring.append(allmatch[random_game])
            else:
                i -= 1
        return retstring
    # end of 2nd if
    else:
        return allmatch
# end of get_searchreleasedate
########################################################################################################
# !searchlastupdatedate [date1][date2] -> games between those dates
def get_searchlastupdate(args):
    d1 = args[0]
    d2 = args[1]
    cur = dbcon.cursor()
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped, last_update FROM games INNER JOIN stats ON games.idx = stats.idx WHERE release_date >= '{0}' AND release_date <= '{1}'""".format(d1, d2))
    allmatch = cur.fetchall()

    # see if there are more than 12 games
    if(len(allmatch) > 12):
        retstring = []
        store_int = []
        for i in range(12):
            random_game = random.randint(0, len(allmatch) - 1)
            if random_game not in store_int:
                store_int.append(random_game)
                retstring.append(allmatch[random_game])
            else:
                i -= 1
        return retstring
    # end of 2nd if
    else:
        return allmatch
# end of get_searchlastupdate
########################################################################################################
# !topscore -> games above this number, otherwise just the top games
def get_topscore():
    cur = dbcon.cursor()
    cur.execute("""SELECT title, console, genre, total_sales, total_shipped, max(critic_score) FROM games INNER JOIN stats ON games.idx = stats.idx GROUP BY title HAVING max(critic_score) = 10""")
    allmatch = cur.fetchall()
    retlist = []
    for i in range(12):
        retlist.append(allmatch[i])
    return retlist
# end of get_topscore
########################################################################################################
# !bottomscore [opt num] -> bottom games below this num or just bottom gamees
def get_bottomscore(args):
    if args:
        cur = dbcon.cursor()
        tmp = int(args[0]) - 1
        cur.execute("""SELECT title, console, genre, total_sales, total_shipped, max(critic_score) FROM games INNER JOIN stats ON games.idx = stats.idx GROUP BY title HAVING critic_score <= {0}  AND critic_score >= {1}""".format(args[0], tmp))
        allmatch = cur.fetchall()
        retlist = []
        if len(allmatch) > 12:
            for i in range(12):
                retlist.append(allmatch[i])
            return retlist
        else:
            return allmatch
    else:
        cur = dbcon.cursor()
        cur.execute("""SELECT title, console, genre, total_sales, total_shipped, min(critic_score) FROM games INNER JOIN stats ON games.idx = stats.idx GROUP BY title HAVING critic_score >= 0 AND critic_score <= 2""")
        allmatch = cur.fetchall()
        retlist = []
        for i in range(12):
            retlist.append(allmatch[i])
        return retlist
        
# end of bottom score
########################################################################################################
# graph for genre
def get_genregraph():
    cur = dbcon.cursor()
    
    cur.execute("""SELECT genre, count(genre) FROM games GROUP BY genre""")
    
    allmatch = cur.fetchall() # get all matches
    return allmatch
# end of genre graph
########################################################################################################
# graph for console
def get_consolegraph():
    cur = dbcon.cursor()
    
    cur.execute("""SELECT console, count(console) FROM games GROUP BY console""")
    
    allmatch = cur.fetchall() # get all matches
    return allmatch
# end of console graph
########################################################################################################