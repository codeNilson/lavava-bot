import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.cogs import add_cogs

load_dotenv()


TOKEN = os.environ.get("DISCORD_TOKEN")

# intents.message_content = True
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await add_cogs(bot)
    for command in bot.commands:
        print(command.name)
    print("Bot is ready!")


bot.run(TOKEN)
