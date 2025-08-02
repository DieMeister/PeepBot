import discord
from discord.ext import commands

import lib
from lib import logging, load_data

import os
import sqlite3

from tokens import BOTTOKEN


class PeepBot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
                logging.extension_success("bot", "Extension loaded", "setup", file)

        if not os.path.isfile(lib.get.database_path()):
            connection = sqlite3.connect(lib.get.database_path())
            with open(lib.get.database_query()) as f:
                script = f.read()
            connection.executescript(script)
            connection.commit()
            connection.close()

            logging.default_logger("bot", "Bot Database created", "setup", "warn")

        if not os.path.isfile(lib.get.log_path()):
            connection = sqlite3.connect(lib.get.log_path())
            with open(lib.get.log_query()) as f:
                script = f.read()
            connection.executescript(script)
            connection.commit()
            connection.close()

            logging.default_logger("bot", "Logging Database created", "setup", "warn")

        synced = await self.tree.sync()
        logging.sync_commands("setup", len(synced))


lib.config = load_data("./config.json")
logging.default_logger("bot", "Configuration file loaded", "setup")

intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = PeepBot(command_prefix="!", intents=intents, help_command=None)
bot.run(BOTTOKEN)
