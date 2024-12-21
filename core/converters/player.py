from discord.ext import commands
from api.api_client import api_client
import settings


class Player(commands.Converter):
    async def convert(self, ctx, input_value: str):
        """
        Converte o input_value (username ou menção) em um objeto player.
        Se for uma menção, pega o UID do usuário mencionado.
        """
        try:
            # Verifica se é uma menção de um membro do Discord
            if input_value.startswith("<@") and input_value.endswith(">"):
                member_id = input_value[2:-1]  # Remove os caracteres "<@" e ">"
                player = await api_client.get_player_by_uid(
                    member_id
                )  # Usando o UID do membro
            else:
                # Caso contrário, trata como um username
                player = await api_client.get_player_by_user(input_value)

        except settings.LoginError as e:
            settings.LOGGER.error("Erro ao carregar jogador '%s': %s", input_value, e)
            await ctx.send("Erro ao conectar ao servidor. Tente novamente mais tarde.")
            raise commands.CommandError("Falha na conexão com o servidor.")
        except Exception as e:
            settings.LOGGER.exception("Erro ao buscar jogador '%s': %s", input_value, e)
            await ctx.send("Ocorreu um erro. Tente novamente mais tarde.")
            raise commands.CommandError("Erro ao processar a solicitação.")

        if not player:
            settings.LOGGER.info("Jogador '%s' não encontrado.", input_value)
            await ctx.send(
                f"Jogador '{input_value}' não encontrado. Verifique e tente novamente."
            )
            raise commands.BadArgument(f"Usuário '{input_value}' não encontrado.")

        return player
