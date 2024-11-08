import os
import discord
from dotenv import load_dotenv
from core.bot import LavavaBot

load_dotenv()


TOKEN = os.environ.get("DISCORD_TOKEN")

# intents.message_content = True
intents = discord.Intents.all()
bot = LavavaBot(command_prefix="!", intents=intents)

bot.run(TOKEN)
