import discord
from discord.ext import commands

import os

import tokens
import logic


class PeepBot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"Cogs.{file[:-3]}")
        logic.logging("info", "bot", "cogs loaded", {
            "command": False
        })


intents = discord.Intents.all()  # FIXME replace with only needed intents
bot = PeepBot(command_prefix="!", intents=intents, help_command=None)

bot.run(tokens.peep_bot)
