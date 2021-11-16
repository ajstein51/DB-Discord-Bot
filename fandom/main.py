# includes
from bs4 import BeautifulSoup # pip install beautifulsoup4
import requests # pip install requests
html = requests.get("https://gamicus.fandom.com/wiki/List_of_banned_video_games").text
soup = BeautifulSoup(html, 'html5lib') # pip install html5lib
import csv
import sqlite3
from sqlite3 import Error

# functions
def getVideoGameDetail():
    fulldetails = []
    for tables in soup.find_all('table'):
        # tables is each table in the webpage
        # loop through each table individually
        for table in tables.find_all('tbody'):
            for som in table.find_all('tr'):
                fulldetails.append(som.text.splitlines(True))
    # end of fors
    
    return fulldetails
# end of function

# parse the line to get the name
def getName(line):
    s1 = ""
    if line[1] != '\n':
        for i in range(0, len(line[1])):
            if line[1][i] != '\n':
                s1 += line[1][i]
    return s1
# end of function

# get the reason 
def getDetail(line):
    s1 = ""
    if line[3] != '\n':
        for i in range(0, len(line[3])):
            if line[3][i] != '\n':
                s1 += line[3][i]

    return s1
# end of function

# create the database file if needed
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
# end of fun

# given the table connection and the name of table
def create_table(dbcon):
    try:
        c = dbcon.cursor()
        tmp = """CREATE TABLE IF NOT EXISTS game (\ngname text,\nreason text NOT NULL\n);"""
        c.execute(tmp)
    except Error as e:
        print(e)
# end of func

# get the parts and put into a csv
def intodb(dbcon, line):
    name = []
    reason = []
    # init = ['Name', 'Reason']
    for game in line:
        name.append(getName(game))
        reason.append(getDetail(game))
    # end of for

    # insert names into the db
    for i in range(0, len(name)):
        cur = dbcon.cursor()
        # sql = "INSERT INTO game (gname, reason)\nVALUES(",name[i], reason[i],")"
        cur.execute("""INSERT INTO game (gname, reason)VALUES (?, ?)""", (name[i], reason[i]))
        dbcon.commit()
# end of func

def delete(dbcon):
    cur = dbcon.cursor()
    cur.execute("""DELETE FROM game WHERE gname='Name'""")
    dbcon.commit()
# end of function

def query(dbcon):
    userinput = input("Whats the query:")
    cur = dbcon.cursor()
    cur.execute(userinput)

# end of fun

# main
def main():
    flag = 0
    # make sql table
    dbcon = create_connection("test1.db")
    if dbcon is not None:
        create_table(dbcon)
    else:
        print("error in making table")
    
    # webscrape
    # get the details 
    fulldetail = getVideoGameDetail()
    
    # insert into a db, stop it from always doing it
    if flag == 0:
        intodb(dbcon, fulldetail)
        # delete the useless row (Name, Reason)
        delete(dbcon)
        flag = 1
    # end of if
    
    query(dbcon)

# end of main

if __name__ == "__main__":
    main()
    