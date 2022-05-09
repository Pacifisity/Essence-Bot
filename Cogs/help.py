import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime
class helpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def cog_check(self, ctx):
        channel1, channel2, channel3 = self.bot.get_channel(735131468145360917), self.bot.get_channel(920479737405644830), self.bot.get_channel(927583858856177694)
        return ctx.channel == channel1 or ctx.channel == channel2 or ctx.channel == channel3
    
async def setup(bot: commands.Bot):
    print("Help Cog Ready")
    await bot.add_cog(helpCommand(bot))
