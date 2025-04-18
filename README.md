# What is this?
This is going to be a fun little discord bot create together with the community of the Sinaheh discord server

# What it does:
An explanation for every command and event.  
The prefix for all PrefixCommands is `!`.  
**DeveloperCommand**s can only be executed by the accounts listed in `data.json["developer"]`;
those commands are always PrefixCommands.

## Bot
This module contains everything concerning the bot itself.

### sync
**PrefixCommand**  
**DeveloperCommand**  
`!sync`  
This command syncs all application commands immediately with discord. 
That should only be needed when a new command is implemented, or when the bot runs for the first time.  

### reload_cog
**PrefixCommand**  
**DeveloperCommand**  
`!reload_cog <extension>`  

This command reloads a cog that is currently loaded.  
`extension` is the cog that is being reloaded if possible.  

Possible answers are:
- "Cog reloaded successfully"
- "Cog does not exist"
- "Cog was not loaded before, try load_cog instead"
- "Cog could not be reloaded"

### load_cog
**PrefixCommand**  
**DeveloperCommand**  
`!load_cog <extension>`  

This command loads a currently unload cog.  
`extension` is the cog that is being loaded if possible.  

Possible answers are:
- "Cog loaded"
- "Cog does not exist"
- "Cog was already loaded"
- "Cog failed to load"

### unload_cog
**PrefixCommand**  
**DeveloperCommand**  
`!unload_cog <extension>`  

This command unloads a currently loaded cog.  
`extension` is the cog that is being unloaded if possible.  

Possible answers are:
- "Cog unloaded"
- "Cog does not exist"
- "Cog was already not loaded"

# Before self-hosting:
- replace `BOTTOKEN` with your BotToken at the end of `main.py`
- replace `data.json["developer"]` with a list of your developer's discord user IDs

## Dependencies
- discord.py
- colorama

## Example formats
you can delete those if you want to
- [log saves](./Logs/example.json)
