########################################################################################################
# AJ Stein
# this file will do the functions for the cmds
# CS 4620 Database
########################################################################################################
# includes
import sqlite3
from sqlite3 import Error
import math

def main():
    # This is the connection to the db
    global dbconnection
    dbconnection = create_connection('game.db')
# end of main

# connect to the db
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
# end of fun

# declaring main
if __name__ == "__main__":
    main()