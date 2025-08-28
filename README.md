This is a DiscordBot created with the help of the members of [sinaheh's community discord server](https://discord.gg/YmKuTTdZFw)

# Usage 
Once the bot is hosted correctly it can be invited to any discord server.
Once on the server channels can be set up where the bot receives valid commands.
This is further explained when executing `/help <setup>` in any channel the bot can access (read and write).  
Using `!psps` a member of the server gets the chance to catch a peep, get scratched by the peep or get nothing.
The probabilities are 1/7, 2/7, and 4/7 - listed in the order they were listed before.  
The commands `/rank` and `/leaderboard` show ones amount of peeps and tries, or the 10 members with the most peeps of the server.

# Dependencies
- discord
- colorama

# When Hosting
Make sure to change `BOTTOKEN` in [main.py](./main.py) to your actual bot token.
No other code changes are required to run the bot,
but it is recommended to change the UserIDs in [config.json](config.json) as well as adding emotes and changing the markdown of them.  
It is still required to [create a discord bot](https://discord.com/developers/applications) that is controlled by the provided code.
