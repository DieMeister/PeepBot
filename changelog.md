# 0.2.0
## Changes

- change probability to catch a peep from 2% to 1/7 (~14%)
- change probability to get scratched from 32% to 2/7 (~29%)

## Added Features

- add leaderboard command
- add rank command
- peeps get stolen 1% of the time a peep is caught
- hidden cat-command
- Commands to assign roles
  - Admin Command to add a Role to the List
  - Admin Command to remove a Role from the List
  - Manager Command to give a Member a Role from the List
  - Manager Command to remove a Role from the List from a Member
  - Command to send Logs in a Discord Channel for these actions

## Removed Features

- remove special message for addie's first peep
  - addie got a peep

## Code Changes

- change variable name of the BotToken
- switch from json to sqlite3 as database
  - effecting everything but [configuration data](config.json)
- add type annotations to all functions
- refactoring of almost everything
