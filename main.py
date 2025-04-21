import discord
from discord.ext import commands

import os

import tokens
import logic


class PeepBot(commands.Bot):
	async def setup_hook(self) -> None:
		for file in os.listdir("./Cogs"):
			if file.endswith(".py"):
				await self.load_extension(f"Cogs.{file[:-3]}")
		logic.logging("info", "bot", "cogs loaded", {
			"command": False
		})

		logic.data = logic.load_data(logic.database_path)
		logic.embeds = logic.load_data("Data/embeds.json")
		logic.logging("info", "bot", "database loaded", {
			"command": False
		})


intents = discord.Intents.all()
bot = PeepBot(command_prefix="!", intents=intents, help_command=None)

bot.run(tokens.butter_test)  # FIXME create BotToken


# TODO move data files in separate folder
