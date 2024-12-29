import random
import discord
from discord.ui import Select


class SelectMap(Select):
    def __init__(
        self,
        *,
        placeholder="Selecione um mapa",
        options=None,
        cog,
    ):
        self.cog = cog
        self.captain_choices = {
            "blue_team_map": None,
            "red_team_map": None,
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
            options=options,
        )

    async def callback(self, interaction):

        selected_map = self.values[0]

        if interaction.user.id == self.cog.captain_blue.discord_uid:
            self.captain_choices["blue_team_map"] = selected_map
        else:
            self.captain_choices["red_team_map"] = selected_map

        await interaction.response.send_message(
            f"Você escolheu o mapa {selected_map}.", ephemeral=True
        )

        if (
            self.captain_choices["blue_team_map"]
            and self.captain_choices["red_team_map"]
        ):
            final_map_choice = self.choose_random_map()
            self.view.final_map_choice = final_map_choice
            self.view.stop()

    async def interaction_check(  # pylint: disable=arguments-differ
        self, interaction: discord.Interaction
    ) -> bool:

        captain_blue = self.cog.captain_blue.discord_uid
        captain_red = self.cog.captain_red.discord_uid

        user_is_captain = interaction.user.id in [captain_blue, captain_red]

        if not user_is_captain:
            await interaction.response.send_message(
                "Somente os capitães podem escolher o mapa.",
                ephemeral=True,
                delete_after=5,
            )
            return False

        if (
            interaction.user.id == captain_blue
            and self.captain_choices["blue_team_map"]
        ):
            await interaction.response.send_message(
                "Você já escolheu um mapa.", ephemeral=True, delete_after=3
            )
            return False

        if interaction.user.id == captain_red and self.captain_choices["red_team_map"]:
            await interaction.response.send_message(
                "Você já escolheu um mapa.", ephemeral=True, delete_after=3
            )
            return False

        return True

    def choose_random_map(self):
        list_maps = list(self.captain_choices.values())
        final_map_choice = random.choice(list_maps)

        return final_map_choice
