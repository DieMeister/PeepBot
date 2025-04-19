# What is this?
This is going to be a fun little discord bot create together with the community of the Sinaheh discord server

# What it does:
An explanation for every command and event.  
The prefix for all PrefixCommands is `!`.  
**DeveloperCommand**s can only be executed by the accounts listed in `data.json["developer"]`.
Who has the right to execute **ApplicationCommand**s can be changed in the server settings.

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

## TwitchCommands
This module contains commands known from sinaheh's Twitch chat as well as functionality directly linked to them.  
The following commands are supported:  
- `!ao3`
- `!patreon`
- `!pinterest`
- `!prints`
- `!socials`
- `!spotify`
- `!tiktok`
- `!twitter`
- `!wishlist`
- `!art`
- `!brush`
- `!comms`
- `!ocs`
- `!ocmusic`
- `!pronouns`
- `!webtoon`

### add_twitch_commands_role
**ApplicationCommand**  
**ManagerCommand**  
`/add_twitch_commands_role <role>`  

This command adds a role to the list of roles that can execute TwitchCommands.  
`role` is the role that is being added.  

Possible answers are:
- "Role added to list"
- "Role can already execute Twitch commands"

### remove_twitch_commands_role
**ApplicationCommand**  
**ManagerCommand**  
`/remove_twitch_commands_role <role>`  

This command removes a role from the list of roles that can execute TwitchCommands.  
`role` is the role that is being removed.  

Possible answers are:
- "Role removed from list"
- "Role was not able to execute commands before anyway"

### list_twitch_command_roles
**ApplicationCommand**  
**ManagerCommand**  
`/list_twitch_command_roles`  

This command replies with a message containing every role that is allowed to execute TwitchCommands.

# Before self-hosting:
- replace `BOTTOKEN` with your BotToken at the end of `main.py`
- replace `data.json["developer"]` with a list of your developer's discord user IDs

## Dependencies
- discord.py
- colorama

## Example formats
you can delete those if you want to
- [log saves](./Logs/example.json)
