import asyncio
import json
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
from chat.gptclient import GPTClient
from scraper.scraper import fetch_latest_game_info

load_dotenv()

with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
SUMMONER_URL = config['summoner_url']

class LowbobDetector(commands.Cog):
    def __init__(self, bot, gpt_api_key):
        self.bot = bot
        self.gpt_client = GPTClient(gpt_api_key)
        self.last_match_id = None
        self.bg_task = self.bot.loop.create_task(self.check_new_game())

    def cog_unload(self):
        self.bg_task.cancel()

    async def check_new_game(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            try:
                loop = asyncio.get_event_loop()

                with open('config/channels.json', 'r', encoding='utf-8') as f:
                    guild_channel_map = json.load(f)
                channel_ids = list(guild_channel_map.values())
                channels = [self.bot.get_channel(cid) for cid in channel_ids if self.bot.get_channel(cid) is not None]

                match_id, ai_score, champ_name, kda, result = await loop.run_in_executor(None, fetch_latest_game_info)

                print(f"{datetime.now().strftime('%H:%M:%S')} - Last game stats: Game ID: {match_id} Champion: {champ_name} KDA:{kda} AI-Score: {ai_score} Result: {result}")
                print(f"{datetime.now().strftime('%H:%M:%S')} - Channels: {[ch.name for ch in channels]}")
                if match_id and match_id != self.last_match_id:
                    if self.last_match_id is not None:
                        ai_text = await loop.run_in_executor(
                            None, self.gpt_client.get_ai_announcement, champ_name, kda, ai_score, result
                        )

                        msg = f"{ai_text}\n<{SUMMONER_URL}>"
                        for ch in channels:
                            await ch.send(msg)
                        print(f"{datetime.now().strftime('%H:%M:%S')} - Message: {msg}")

                    self.last_match_id = match_id
                    print(f"{datetime.now().strftime('%H:%M:%S')} - New match found.")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - No new match found.")

            except Exception as e:
                print(f"Error in background task: {e}")

            await asyncio.sleep(150)

async def setup(bot):
    from os import getenv
    gpt_key = getenv("OPENAI_API_KEY")
    await bot.add_cog(LowbobDetector(bot, gpt_key))
