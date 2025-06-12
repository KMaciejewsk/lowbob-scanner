import discord
from discord.ext import commands
import time
import json
import os
from chat.gptclient import GPTClient

class ReplyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gpt = GPTClient(os.getenv("OPENAI_API_KEY"))
        self.reply_users = self.load_users()
        self.last_reply_time = {}  # {user_id: timestamp}

    def load_users(self):
        with open("config/users.json", 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_users(self):
        with open("config/users.json", 'w', encoding='utf-8') as f:
            json.dump(self.reply_users, f, indent=4)

    @commands.command(name="addreply")
    async def addreply(self, ctx, user: discord.User):
        if user.id not in self.reply_users["users"]:
            self.reply_users["users"].append(user.id)
            self.save_users()
            await ctx.send(f"✅ Lowbob scanner will now reply to {user.name}.")
        else:
            await ctx.send(f"ℹ️ Lowbob scanner is already replying to {user.name}.")

    @commands.command(name="removereply")
    async def removereply(self, ctx, user: discord.User):
        if user.id in self.reply_users["users"]:
            self.reply_users["users"].remove(user.id)
            self.save_users()
            await ctx.send(f"❌ Lowbob scanner will now stop replying to {user.name}.")
        else:
            await ctx.send(f"ℹ️ Lowbob scanner is not replying to {user.name}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('config/channels.json', 'r', encoding='utf-8') as f:
            guild_channel_map = json.load(f)
        channel_ids = list(guild_channel_map.values())
        channels = [self.bot.get_channel(cid) for cid in channel_ids if self.bot.get_channel(cid) is not None]

        if message.author.bot or message.channel not in channels:
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        user_id = message.author.id
        now = time.time()

        if user_id in self.reply_users["users"]:
            last_time = self.last_reply_time.get(user_id, 0)
            if now - last_time >= 60:
                self.last_reply_time[user_id] = now

                try:
                    previous_bot_message = ""
                    async for msg in message.channel.history(limit=50, before=message.created_at):
                        if msg.author == self.bot.user:
                            previous_bot_message = msg.content
                            break

                    reply = await self.bot.loop.run_in_executor(
                        None,
                        self.gpt.get_reply_to_message,
                        message.author.display_name,
                        message.content,
                        previous_bot_message
                    )

                    if reply:
                        await message.channel.send(reply)

                except Exception as e:
                    print(f"GPT reply failed: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(ReplyCog(bot))
