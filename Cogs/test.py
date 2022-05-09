import discord
from discord.ext import commands

class Test(commands.Cog): #Test
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        embed = discord.Embed(description="cringe")
        embed.add_field(value=f"hemlok smol brain")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    print("Test Cog Ready")
    await bot.add_cog(Test(bot), guilds=[discord.Object(id=725164114506285066)])