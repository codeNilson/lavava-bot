import discord
from discord.ui import Button
from utils import ChannelID, RoleID
from utils.admin import move_user_to_channel
from api import models


class PlayerButton(Button):
    def __init__(self, *, player: models.PlayerModel):
        super().__init__(
            label=player.username,
            style=discord.ButtonStyle.secondary,
            custom_id=player.username,
        )
        self.player = player

    async def callback(self, interaction: discord.Interaction):

        current_captain = (
            self.view.cog.captain_blue
            if self.view.cog.is_blue_captain_turn
            else self.view.cog.captain_red
        )
        next_captain = (
            self.view.cog.captain_red
            if self.view.cog.is_blue_captain_turn
            else self.view.cog.captain_blue
        )

        blue_channel = interaction.guild.get_channel(ChannelID.BLUE.value)
        red_channel = interaction.guild.get_channel(ChannelID.RED.value)

        blue_role = interaction.guild.get_role(RoleID.BLUE.value)
        red_role = interaction.guild.get_role(RoleID.RED.value)

        # add player to the team of the current captain
        team = (
            self.view.cog.team_blue
            if self.view.cog.is_blue_captain_turn
            else self.view.cog.team_red
        )
        team.add_player(self.player)

        # remove player from the list of available players
        self.view.cog.players.remove(self.player)

        # add role and move player to the channel
        member = await self.player.to_member(interaction)
        if member:
            channel = (
                blue_channel if self.view.cog.is_blue_captain_turn else red_channel
            )
            await member.add_roles(
                blue_role if self.view.cog.is_blue_captain_turn else red_role
            )
            await move_user_to_channel(member, channel)

        for button in self.view.children:
            if button.custom_id == self.player.username:
                button.disabled = True
                button.style = (
                    discord.ButtonStyle.primary
                    if current_captain == self.view.cog.captain_blue
                    else discord.ButtonStyle.danger
                )

        # if the teams are full, show the teams and create the match
        if self._all_teams_if_full():
            await interaction.response.edit_message(
                content="Todos os jogadores foram escolhidos!", view=self.view
            )
            self.view.stop()

        # if the team is not full change the current captain and start again the process
        # this lets the captain of team red to choose two players in a row if there's only three remaining players
        else:
            if len(self.view.cog.team_red.players) != 4:
                next_captain = (
                    self.view.cog.captain_red
                    if self.view.cog.is_blue_captain_turn
                    else self.view.cog.captain_blue
                )
                self.view.cog.is_blue_captain_turn = (
                    not self.view.cog.is_blue_captain_turn
                )
                emoji = "🔵" if self.view.cog.is_blue_captain_turn else "🔴"
                message_content = f"Jogador {self.player.mention} foi escolhido! Agora é a vez de {emoji + next_captain.mention} escolher."
            else:
                message_content = f"Jogador {self.player.mention} foi escolhido! 🔴{current_captain.mention}, você tem o direito a mais uma escolha."

            await interaction.response.edit_message(
                content=message_content,
                view=self.view,
            )

    def _all_teams_if_full(self):
        """Check if the teams are full"""
        if (
            len(self.view.cog.team_blue.players) == 5
            and len(self.view.cog.team_red.players) == 5
        ):
            return True
        return False
