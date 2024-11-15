import discord
from discord.ext import commands
from discord.ui import Button, View


class Teste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def teste(self, ctx):
        botao1 = Button(
            style=discord.ButtonStyle.green, label="Aro Might", custom_id="aro_might"
        )
        botao2 = Button(
            style=discord.ButtonStyle.red, label="Taifuzinha", custom_id="taifuzinha"
        )

        async def callback_botao(interaction):
            print(interaction.is_expired())

            if interaction.data.get("custom_id") == "aro_might":
                # await interaction.response.edit_message(content="Você clicou neste botão!", delete_after=5)
                # await interaction.followup.send("Aro Might é o melhor!")
                # await interaction.message.add_reaction("")
                await interaction.message.edit(delete_after=60)
                await interaction.response.send_message("Aro Might é o melhor!")
            else:
                # await interaction.response.send_modal("Taifuzinha é o melhor!")
                await interaction.response.send_message("Taifuzinha é o melhor!")

        botao1.callback = callback_botao
        botao2.callback = callback_botao

        view = View(timeout=20)
        view.add_item(botao1)
        view.add_item(botao2)

        await ctx.send("Quem é o melhor?", view=view)
