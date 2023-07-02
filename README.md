# Albion-discord-bot-v2
version 2 of my first bot https://github.com/ScrappieG/Albion-discord-bot this one is more simple but is alot better because of it

This bot is still being worked on and tested and is the version
2.0 of the other bot I made which was a little over kill for what
we were trying to do. If you are interested in these things I 
definitly recommed you go check it out https://github.com/ScrappieG/Albion-discord-bot

any questions feel free to reach out to me at stone#3650

# about

This bot was created for an albion online guild server. It allows
for easier lootsplits and regears. The bot tracks how much the 
guild owes each member which is super useful if you do things
like regearing people and the guild buying lootsplits.
This is still a work in progress and I will be adding more features
to it. You guys are welcome to use it just gimme some credit thats all
i ask :D.

# Bot Commands

Bot commands

/register <member>

/regear <member><tier> Optional:<Alt value>

/update_balance <member><ammount>

/all_balances 

/t5_flat_craft <first_name> <last_name> <tier> <material_1> <material_2> Optional:<return_rate>

/bannana 🙀

/lootsplit <lootsplit total><# of people>

# Bot Apps

View join date

View guild balance


#API credit
Albion data project Docs https://www.albion-online-data.com/api/swagger/index.html

#setting up

Steps:

1. Put your Bot token in main.py

2. Put your discord server id in main.py (this is done by right clicking the server icon)

3. Create a log channel for the bot and add it to main.py

4. Set up The sql data base

5. Run it and invite it to your server and you should be all set

#setting up sqlite database

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
discord_id TEXT NOT NULL,
guild_silver_balance int DEFAULT '0', display_name string);
CREATE TABLE sqlite_sequence(name,seq);
