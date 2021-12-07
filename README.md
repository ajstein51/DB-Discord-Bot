# Game Sales Discord Bot



## Project Description
This project takes a CSV files from kaggle and implemented a UI to query from it from discord. Using discords API (version 1.0) I made a bot called 'GameInfo' that has severial query options that range from text response, image response, and graph response. Types of information that you can get from the bot include: publisher, developer, release date, last update, console, genre, total sales, and more.

## Tools
* Discord API
    * Making the bot and UI
* Github
    * Version Control
* AWS (EC2)
    * Bot hosting
* Pandas
    * Converting the CSV to a database
* BeautifulSoup
    * Webscraping wiki for more info and cover arts
* SQLITE

## Installing Dependencies
To install all python dependencies run the following commands:
```
pip install -U discord.py
pip install -U python-dotenv
pip install matplotlib
pip install regex
```
If you want to run the makedb.ipynb file then you will also need the below packages. I don't recomend running that file as the webscraping is terribly inefficient and took 8 hours.
```
pip install pandas
pip install jupyterlab
pip install requests
pip install beautifulsoup4
```

## Running Locally
First download the repo and you will see a file named '.env' from the discord_bot folder. Within that file you will have to put your discord bots token. To make the discord bot itself to get the token you will have to go to discords developer portal and register one. Once you have placed the token you will need to invite your bot to a server that you have admin permission within. To invite use the following link, put your bots client ID in the brackets:
https://discord.com/oauth2/authorize?client_id=[CLIENT ID HERE]&scope=bot
Finally you are set up and to have to bot go online run this command within your bots directory:
```
python3 bot.py
```

Notice: If this didnt make a ton of sense follow discords documentation here:
https://discordpy.readthedocs.io/en/stable/discord.html

## Running from my host
I have set up this bot on AWS EC2, I cant promise the bot will always be online however. To invite the bot from that instance copy and paste this link into your browser and invite it to a server you have admin permissions within:
https://discord.com/oauth2/authorize?client_id=917518284054757426&scope=bot
