import discord
from discord.ext import commands

import lib
from lib import logging
from lib.logging import Module, ExecutionMethod, LogType

import os
import sqlite3

from tokens import BOTTOKEN


class PeepBot(commands.Bot):
    async def setup_hook(self) -> None:
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
                logging.extension_success(Module.BOT, "Extension loaded", ExecutionMethod.SETUP, file)

    @staticmethod
    async def on_ready() -> None:
        logging.default_logger(Module.BOT, "Bot is ready", ExecutionMethod.SETUP)


if __name__ == "__main__":
    if not os.path.isfile(lib.get.log_path()):
        with open(lib.get.log_query()) as f:
            script = f.read()
        log_db = sqlite3.connect(lib.get.log_path())
        log_db.executescript(script)
        log_db.commit()
        log_db.close()

        logging.default_logger(Module.BOT, "Logging Database created", ExecutionMethod.SETUP, LogType.WARN)

    if not os.path.isfile(lib.get.database_path()):
        with open(lib.get.database_query()) as f:
            script = f.read()
        data_db = sqlite3.connect(lib.get.database_path())
        data_db.executescript(script)
        data_db.commit()
        data_db.close()

        logging.default_logger(Module.BOT, "Bot Database created", ExecutionMethod.SETUP, LogType.WARN)

    intents = discord.Intents.none()
    intents.guild_messages = True
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    bot = PeepBot(command_prefix=("!pb!", "?", "!"), intents=intents, help_command=None)
    bot.run(BOTTOKEN)
