import discord
from discord.ext import commands

import os
import sqlite3
from lib.json_data import load_data

from tokens import BOTTOKEN
import logic


class PeepBot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
        logic.logging("info", "bot", "cogs loaded", {
            "command": False
        })

        if not os.path.isfile(logic.config["file_paths"]["database"]):
            connection = sqlite3.connect(logic.config["file_paths"]["database"])
            with open("sql/tables.sql") as f:
                script = f.read()
            connection.executescript(script)
            connection.commit()
            connection.close()
            logic.logging("warn", "bot", "Database created", {
                "command": False
            })

        synced = await self.tree.sync()
        logic.logging("info", "bot", "Commands synced", {
            "amount": len(synced),
            "command": False
        })


logic.config = load_data("./config.json")
logic.logging("info", "bot", "configurations loaded", {
    "command": False
})

intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = PeepBot(command_prefix="!", intents=intents, help_command=None)
bot.run(BOTTOKEN)
