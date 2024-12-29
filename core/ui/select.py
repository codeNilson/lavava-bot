import random
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
        self.captain_choices = {
            "blue_choice": None,
            "red_choice": None,
        }
        options = options or [
            discord.SelectOption(label="Haven", value="Haven"),
            discord.SelectOption(label="Icebox", value="Icebox"),
            discord.SelectOption(label="Pearl", value="Pearl"),
            discord.SelectOption(label="Sunset", value="Sunset"),
            discord.SelectOption(label="Lotus", value="Lotus"),
            discord.SelectOption(label="Abyss", value="Abyss"),
            discord.SelectOption(label="Breeze", value="Breeze"),
            discord.SelectOption(label="Bind", value="Bind"),
            discord.SelectOption(label="Fracture", value="Fracture"),
            discord.SelectOption(label="Split", value="Split"),
            discord.SelectOption(label="Ascent", value="Ascent"),
        ]
        super().__init__(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )

    async def callback(self, interaction):

        choice = self.values[0]

        if interaction.user.id == self.cog.captain_blue.discord_uid:
            self.captain_choices["blue_choice"] = choice
        else:
            self.captain_choices["red_choice"] = choice

        await interaction.response.send_message(
            f"Você escolheu o mapa {choice}.", ephemeral=True
        )

        if self.captain_choices["blue_choice"] and self.captain_choices["red_choice"]:
            map_chosen = self.random_map()
            self.view.map_chosen = map_chosen
            self.view.stop()

    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:  # pylint: disable=arguments-differ

        captain_blue = self.cog.captain_blue.discord_uid
        captain_red = self.cog.captain_red.discord_uid

        is_captain = interaction.user.id in [captain_blue, captain_red]

        if not is_captain:
            await interaction.response.send_message(
                "Somente os capitães podem escolher o mapa.",
                ephemeral=True,
                delete_after=5,
            )
            return False

        if interaction.user.id == captain_blue and self.captain_choices["blue_choice"]:
            await interaction.response.send_message(
                "Você já escolheu um mapa.", ephemeral=True, delete_after=3
            )
            return False

        if interaction.user.id == captain_red and self.captain_choices["red_choice"]:
            await interaction.response.send_message(
                "Você já escolheu um mapa.", ephemeral=True, delete_after=3
            )
            return False

        return True

    def random_map(self):
        list_maps = list(self.captain_choices.values())
        map_chosen = random.choice(list_maps)

        return map_chosen
