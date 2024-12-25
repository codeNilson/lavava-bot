import discord
from discord.ui import View


class PlayersView(View):
    def __init__(self, timeout: int = 180):
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
