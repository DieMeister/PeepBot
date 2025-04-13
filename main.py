import discord
from discord.ext import commands
import os


class PeepBot(commands.Bot):
	async def setup_hook(self) -> None:
		for file in os.listdir("./Cogs"):
			if file.endswith(".py"):
				await self.load_extension(f"Cogs.{file[:-3]}")


intents = discord.Intents.all()
bot = PeepBot(command_prefix="!", intents=intents)

bot.run(BOTTOKEN)  # FIXME create BotToken