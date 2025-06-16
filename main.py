import discord
from discord.ext import commands

import os

import tokens
import logic


class PeepBot(commands.Bot):
    async def setup_hook(self):
        # load every extension
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
        logic.logging("info", "bot", "cogs loaded", {
            "command": False
        })
        # load database
        logic.data = logic.load_data(logic.database_path)
        logic.logging("info", "bot", "database loaded", {
            "command": False
        })


intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True

bot = PeepBot(command_prefix="!", intents=intents, help_command=None)
bot.run(tokens.peep_bot)
