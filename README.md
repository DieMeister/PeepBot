This is a DiscordBot created with the help of the members of [sinaheh's community discord server](https://discord.gg/YmKuTTdZFw)

# Dependencies
- discord
- colorama

# Before self-hosting
1. create your own discord bot using the [developer portal](https://discord.com/developers/applications)
2. copy and modify the source code
  - copy the repository to your machine (there are multiple possible ways)
    - using git
      - install git on your machine
      - open the terminal
      - navigate to the folder you want the repository to be located in (cd to change folder)
      - git clone https://github.com/DieMeister/PeepBot.git
    - downloading the folder
      - there's a button somewhere on this page to download the repository as `.zip`
      - extract the `.zip` file in the folder you want the repository to be located
  - create `tokens.py` in the home directory (the one this file is located)
    - add the bot token to `tokens.py`, this should look like this (`<your BotToken>` should obviously be your actual bot token):

```python
BOTTOKEN = "<your BotToken>"
```
**UNDER NO CIRCUMSTANCES EVER SHARE THIS WITH ANYONE; IF YOU DID, CHANGE IT IMMEDIATELY**

- create a virtual environment (venv)
  - install all packages the bot relies on
  - change the developer IDs in [data.json](./data.json) with the IDs of you and whoever is a developer of your bot

# Logging
This bot uses a custom logging function ([logic.py](./logic.py).logging) that both prints a short log to the terminal and saves a more detailed log in a json file.  
The urgency of a log entry is defined by its type:

| type  | explanation                                                                                      |
|-------|--------------------------------------------------------------------------------------------------|
| info  | everything works as expected                                                                     |
| warn  | something is odd but it doesn't affect the overall functionality                                 |
| error | something went wrong leading to significantly worse functionality                                |
| fatal | something went wrong leading to an unplanned shutdown or the inability to run even core features |
| debug | only for debugging purposes, should not be in the final code                                     |

The modules of the bot must be defined first and hardcoded into the logging function