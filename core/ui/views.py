import discord
from discord.ui import View
from core.ui.buttons import PlayerButton
from api import models


class PlayersView(View):
    def __init__(self, *, cog, timeout: int = 180):
        self.cog = cog
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        """Callback executado quando a view expira."""
        for child in self.children:
            child.disabled = True
            child.style = discord.ButtonStyle.secondary

        await self.message.edit(
            content="⏳ Tempo esgotado! Nem todos os jogadores foram escolhidos.",
            view=self,
        )

    async def add_player_button(self, *, player: models.PlayerModel):
        button = PlayerButton(player=player)
        self.add_item(button)

    async def interaction_check(self, interaction):  # pylint: disable=arguments-differ

        current_captain = (
            self.cog.captain_blue
            if self.cog.is_blue_captain_turn
            else self.cog.captain_red
        )

        # if the player is not the current captain then return False
        if interaction.user.id != current_captain.discord_uid:
            await interaction.response.send_message(
                "Não é sua vez de escolher!",
                ephemeral=True,
                delete_after=5,
            )
            return False
        return True
