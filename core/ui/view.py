from discord.ui import View
from discord.ext import commands


class PlayersView(View):
    def __init__(self, ctx: commands.Context, timeout: int) -> None:
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.timed_out = False

    async def on_timeout(self):
        print("Timeout")
        self.timed_out = True
        for child in self.children:
            child.disabled = True
        # await self.ctx.send(
        #     "⏳ Tempo esgotado! Nem todos os jogadores foram escolhidos.", view=self
        # )
