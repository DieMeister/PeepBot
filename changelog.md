# 0.4.0
## Features

- Users Database
  - Count of Peeps someone stole
- Anyone can see other Members rank using `/rank <member>` and not just their own
- Log when bot is ready
- `?` and `!pb!` are now supported prefixes too
- DeveloperCommand to give peeps to a member
- DeveloperCommand to remove peeps from a member

## Fixes

- Adds missing letter in help message

## Changes

- Doesn't sync commands everytime the bot starts
- LogMessage when a Member is added to the database is now `Member added to Database` instead of `Member joined Guild`

# 0.3.1
## Fixes

- Sent and received peeps are now tracked correctly and don't show only the last amount someone sent, got

# 0.3.0
## Fixes

- Updates both HelpCommands to be correct again
- Adds Guilds  and Members only when necessary
  - Makes sure they exist then
  - Reduces unnecessary DatabaseEntries

## Features

- Adds a Command to transfer own Peeps to another Member of the same Guild
  - adds received and sent peeps to `/rank` and `/leaderboard` messages
- Funne can be a Thief too now

## Changes

- Moves `possible_role_id()` and `role_in_database()` from `Cogs/Moderation.py` to `lib/checks.py`
- Renames `role_in_database()` to `assignable_role_in_database()` in `lib/checks.py`
- Moves `Cogs/Moderation.Moderation.autocomplete()` to `lib/autocomplete/moderation.autocomplete()`
- Moves `Cogs/Moderation.Moderation.add_assignable_role()` to `Cogs/Config.Config.add_assignable_role()`
- Moves `Cogs/Moderation.Moderation.remove_assignable_role()` to `Cogs/Config.Config.remove_assignable_role()`
- Moves `Cogs/Moderation.Moderation.set_log_channel()` to `Cogs/Config.Config.set_log_channel()`
- Change to Enums to configure LoggingCategories

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
