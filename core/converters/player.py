import discord
from discord.ext import commands
from api.api_client import api_client
import settings


class Player(commands.Converter):
    async def convert(self, interaction: discord.Interaction, member: discord.Member):
        """
        Converte o input_value (username ou menção) em um objeto player.
        Se for uma menção, pega o UID do usuário mencionado.
        """
        try:
            # Verifica se é uma menção de um membro do Discord
            member_uid = member.mention[2:-1]  # Remove os caracteres "<@" e ">"
            player = await api_client.get_player_by_uid(
                member_uid
            )  # Usando o UID do membro
            if not player:
                interaction.response.send_message(
                    "Não foi possível encontrar o jogador informado."
                )
            return player

        except settings.LoginError as e:
            settings.LOGGER.error(
                "Erro ao carregar jogador '%s': %s", member.display_name, e
            )
            await interaction.response.send_message(
                "Erro ao conectar ao servidor. Tente novamente mais tarde."
            )
            raise
        except Exception as e:
            settings.LOGGER.exception(
                "Erro ao buscar jogador '%s': %s", member.display_name, e
            )
            await interaction.response.send_message(
                "Ocorreu um erro. Tente novamente mais tarde."
            )
            raise commands.CommandError("Erro ao processar a solicitação.")
