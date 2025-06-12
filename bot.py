import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    await bot.load_extension("cogs.setchannel")
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.lowbob")

def load_channels():
    if os.path.exists("config/channels.json"):
        with open("config/channels.json", "r") as f:
            return json.load(f)
    return {}

def save_channels(data):
    with open("config/channels.json", "w") as f:
        json.dump(data, f, indent=4)

bot.channels = load_channels()
bot.save_channels = lambda: save_channels(bot.channels)

bot.run(DISCORD_TOKEN)
