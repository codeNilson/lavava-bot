import discord
from discord.ui import Select


class SelectMap(Select):
    def __init__(
        self,
        *,
        placeholder="Selecione um mapa",
        min_values=1,
        max_values=1,
        options=None,
        cog,
    ):
        self.cog = cog
        options = options or [
            discord.SelectOption(label="Haven", value="haven"),
            discord.SelectOption(label="Abyss", value="abyss"),
            discord.SelectOption(label="Split", value="split"),
            discord.SelectOption(label="Fracture", value="fracture"),
            discord.SelectOption(label="Ascent", value="ascent"),
        ]
        super().__init__(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )

    async def callback(self, interaction):
        interaction.response.send_message(
            f"Você escolheu o mapa {interaction.data['values'][0]}.", ephemeral=True
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        captain_blue = self.cog.captain_blue.discord_uid
        captain_red = self.cog.captain_red.discord_uid

        is_captain = interaction.user.id in [captain_blue, captain_red]

        if not is_captain:
            await interaction.response.send_message(
                "Somente os capitães podem escolher o mapa.", ephemeral=True
            )
            return False

        return True
