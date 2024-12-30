import logging
from logging.handlers import TimedRotatingFileHandler
import os
import discord
from dotenv import load_dotenv
from core.bot import LavavaBot

load_dotenv()


TOKEN = os.environ.get("DISCORD_TOKEN")

handler = TimedRotatingFileHandler(
    "logs/discord_bot.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
handler.setLevel(logging.INFO)
discord.utils.setup_logging(handler=handler)

intents = discord.Intents.all()
bot = LavavaBot(intents=intents)

bot.run(TOKEN)
