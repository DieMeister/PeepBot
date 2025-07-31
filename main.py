import discord
from discord.ext import commands

from lib import logging
from lib.json_data import load_data

import os
import sqlite3

from tokens import BOTTOKEN
import logic


class PeepBot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
                logging.extension_success("bot", "Extension loaded", "setup", file)

        if not os.path.isfile(logic.config["file_paths"]["database"]):
            connection = sqlite3.connect(logic.config["file_paths"]["database"])
            with open("sql/tables.sql") as f:
                script = f.read()
            connection.executescript(script)
            connection.commit()
            connection.close()

            logging.default_logger("bot", "Bot Database created", "setup", "warn")

        if not os.path.isfile(logic.config["file_paths"]["logs"]):
            connection = sqlite3.connect(logic.config["file_paths"]["logs"])
            with open("sql/logging.sql") as f:
                script = f.read()
            connection.executescript(script)
            connection.commit()
            connection.close()

            logging.default_logger("bot", "Logging Database created", "setup", "warn")

        synced = await self.tree.sync()
        logging.sync_commands("setup", len(synced))


logic.config = load_data("./config.json")
logging.default_logger("bot", "Configuration file loaded", "setup")

intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = PeepBot(command_prefix="!", intents=intents, help_command=None)
bot.run(BOTTOKEN)
