import discord
from discord.ui import View, Button
from api import models
from core.ui.embeds import teams_embed
from utils import move_user_to_channel, ChannelID, RoleID


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

    async def add_player_button(self, *, player):
        button = Button(
            label=player.username,
            style=discord.ButtonStyle.secondary,
            custom_id=player.username,
        )

        async def button_callback(
            interaction: discord.Interaction,
            player: models.PlayerModel = player,
        ):
            current_captain = (
                self.cog.captain_blue
                if self.cog.is_blue_captain_turn
                else self.cog.captain_red
            )
            next_captain = (
                self.cog.captain_red
                if self.cog.is_blue_captain_turn
                else self.cog.captain_blue
            )

            blue_channel = interaction.guild.get_channel(ChannelID.BLUE.value)
            red_channel = interaction.guild.get_channel(ChannelID.RED.value)

            blue_role = interaction.guild.get_role(RoleID.BLUE.value)
            red_role = interaction.guild.get_role(RoleID.RED.value)

            # add player to the team of the current captain
            team = (
                self.cog.team_blue
                if self.cog.is_blue_captain_turn
                else self.cog.team_red
            )
            team.add_player(player)

            # remove player from the list of available players
            self.cog.players.remove(player)

            # add role and move player to the channel
            member = await player.to_member(interaction)
            if member:
                channel = blue_channel if self.cog.is_blue_captain_turn else red_channel
                await member.add_roles(
                    blue_role if self.cog.is_blue_captain_turn else red_role
                )
                await move_user_to_channel(member, channel)

            # if the teams are full, show the teams and create the match
            if (
                len(self.cog.team_blue.players) == 5
                and len(self.cog.team_red.players) == 5
            ):
                self.stop()

            # if the team is not full change the current captain and start again the process
            else:
                # this lets the captain of team red to choose two players in a row if there's only three remaining players
                if len(self.cog.team_red.players) != 4:
                    next_captain = (
                        self.cog.captain_red
                        if self.cog.is_blue_captain_turn
                        else self.cog.captain_blue
                    )
                    self.cog.is_blue_captain_turn = not self.cog.is_blue_captain_turn
                    emoji = "🔵" if self.cog.is_blue_captain_turn else "🔴"
                    message_content = f"Jogador {player.mention} foi escolhido! Agora é a vez de {emoji + next_captain.mention} escolher."
                else:
                    message_content = f"Jogador {player.mention} foi escolhido! 🔴{current_captain.mention}, você tem o direito a mais uma escolha."

                for button in self.children:
                    if button.custom_id == player.username:
                        button.disabled = True
                        button.style = (
                            discord.ButtonStyle.primary
                            if current_captain == self.cog.captain_blue
                            else discord.ButtonStyle.danger
                        )

                await interaction.response.edit_message(
                    content=message_content,
                    view=self,
                )

        button.callback = button_callback
        self.add_item(button)

    async def interaction_check(self, interaction):  # pylint: disable=arguments-differ

        current_captain = (
            self.cog.captain_blue
            if self.cog.is_blue_captain_turn
            else self.cog.captain_red
        )

        # if the player is not the current captain then return
        if interaction.user.id != current_captain.discord_uid:
            await interaction.response.send_message(
                "Não é sua vez de escolher!",
                ephemeral=True,
                delete_after=5,
            )
            return False
        return True

    def all_teams_if_full(self):
        """Check if the teams are full"""
        if len(self.cog.team_blue.players) == 5 and len(self.cog.team_red.players) == 5:
            return True
        return False
