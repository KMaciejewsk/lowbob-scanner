from discord.ext import commands
import discord

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"])
    async def commands_list(self, ctx):
        prefix = ">"
        commands = [cmd.name for cmd in self.bot.commands if not cmd.hidden]
        commands.sort()
        commands_str = "\n".join(f"{prefix}{cmd}" for cmd in commands)
        embed = discord.Embed(
            title="Available Commands",
            description=commands_str,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))
