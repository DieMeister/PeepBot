This is a DiscordBot created with the help of the members of [sina's community discord server](https://discord.gg/YmKuTTdZFw)

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
peep_bot = "<your BotToken>"
```
**UNDER NO CIRCUMSTANCES EVER SHARE THIS WITH ANYONE; IF YOU DID, CHANGE IT IMMEDIATELY**

- create a virtual environment (venv)
  - install all packages the bot relies on
  - change the developer IDs in [data.json](./data.json) with the IDs of you and whoever is a developer of your bot
