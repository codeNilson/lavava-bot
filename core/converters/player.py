from discord.ext import commands
from api.api_client import api_client
import settings


class Player(commands.Converter):
    async def convert(self, ctx, username: str):
        """
        Converte o username em um objeto player.
        """
        try:
            player = await api_client.get_player_by_user(username)
        except settings.LoginError as e:
            settings.LOGGER.error(
                "Erro ao tentar carregar o jogador '%s': %s", username, str(e)
            )
            await ctx.send(
                "Erro ao conectar ao servidor. Não é possível carregar os jogadores no momento. Por favor, tente mais tarde."
            )
            raise commands.CommandError("Falha na conexão com o servidor.")
        except Exception as e:
            settings.LOGGER.exception(
                "Erro inesperado ao buscar o jogador '%s': %s", username, str(e)
            )
            await ctx.send(
                "Ocorreu um erro inesperado ao processar o pedido. Por favor, tente novamente mais tarde."
            )
            raise commands.CommandError("Erro inesperado ao processar a solicitação.")

        if not player:
            settings.LOGGER.info("Jogador '%s' não encontrado.", username)
            await ctx.send(
                f"Jogador '{username}' não encontrado. Por favor, verifique o usuário e tente novamente."
            )
            raise commands.BadArgument(
                f"Usuário '{username}' não encontrado na lista de jogadores."
            )

        return player
