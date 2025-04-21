from discord import ui, TextStyle, Interaction, app_commands
from discord.ext import commands

import logic


class WelcomeMessageModal(ui.Modal):
    def __init__(self, user_name, guild_id):
        super().__init__(title="Welcome Message")
        self.user: str = user_name
        self.guild: int = guild_id

        guild_data = logic.get_item(logic.data["guilds"], "guild_id", self.guild)
        self.old_message = guild_data["onboarding"]["welcome_message"]

        if self.old_message:
            placeholder = self.old_message
        else:
            placeholder = f"Hey {self.user}, welcome in this server!"

        self.new_message = ui.TextInput(label="New Welcome Message",
                                   style=TextStyle.paragraph,
                                   placeholder=placeholder,
                                   required=True)
        self.add_item(self.new_message)

    async def on_submit(self, interaction: Interaction) -> None:
        guild_data = logic.get_item(logic.data["guilds"], "guild_id", interaction.guild_id)
        guild_data["onboarding"]["welcome_message"] = self.new_message.value
        logic.save_data(logic.data, logic.database_path)

        logic.logging("info", "boarding", "Welcome Message changed", {
            "old_message": self.old_message,
            "new_message": self.new_message.value,
            "command": {
                "guild": interaction.guild_id,
                "channel": interaction.channel.id,
                "user": interaction.user.id,
                "type": "ManagerCommand"
            }
        })
        await interaction.response.send_message("Welcome Message changed", ephemeral=True)


class Onboarding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="change_welcome_message", description="Change the WelcomeMessage")
    @app_commands.default_permissions(manage_guild=True)
    async def change_welcome_message(self, interaction: Interaction):
        await interaction.response.send_modal(WelcomeMessageModal(interaction.user.display_name, interaction.guild_id))


async def setup(bot):
    await bot.add_cog(Onboarding(bot))
