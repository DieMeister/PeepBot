import discord
from discord.ext import commands

import lib
from lib import logging, config

import os
import sqlite3

from tokens import BOTTOKEN


class PeepBot(commands.Bot):
    async def setup_hook(self) -> None:
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
                logging.extension_success("bot", "Extension loaded", "setup", file)

    @staticmethod
    async def on_ready() -> None:
        logging.default_logger("bot", "Bot is ready", "setup")


if __name__ == "__main__":
    if not os.path.isfile(config.log_db_path()):
        with open(config.log_db_query_path()) as f:
            script = f.read()
        log_db = sqlite3.connect(config.log_db_path())
        log_db.executescript(script)
        log_db.commit()
        log_db.close()

        logging.default_logger("bot", "Logging Database created", "setup", "warn")

    if not os.path.isfile(config.data_db_path()):
        with open(config.data_db_query_path()) as f:
            script = f.read()
        data_db = sqlite3.connect(config.data_db_path())
        data_db.executescript(script)
        data_db.commit()
        data_db.close()

        logging.default_logger("bot", "Bot Database created", "setup", "warn")

    intents = discord.Intents.none()
    intents.guild_messages = True
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    bot = PeepBot(command_prefix=("!pb!", "?", "!"), intents=intents, help_command=None)
    bot.run(BOTTOKEN)
