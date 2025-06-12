from discord.ext import commands

class SetChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setchannel")
    async def set_channel(self, ctx):
        guild_id = str(ctx.guild.id)
        self.bot.channels[guild_id] = ctx.channel.id
        self.bot.save_channels()
        await ctx.send(f"✅ Lowbob scanner has arrived in {ctx.channel.mention}.")

    @commands.command(name="unsetchannel")
    async def unset_channel(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.channels:
            del self.bot.channels[guild_id]
            self.bot.save_channels()
            await ctx.send(f"❌ Lowbob scanner has left {ctx.channel.mention}.")
        else:
            await ctx.send("⚠️ Lowbob scanner is not here yet.")

async def setup(bot):
    await bot.add_cog(SetChannel(bot))
