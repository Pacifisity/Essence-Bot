import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Item(commands.Cog, app_commands.Group):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Use an item")
    async def use(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        arg = str.lower(arg)
        timestamp = round(datetime.now().timestamp())
        with sqlite3.connect('DB Storage/essence.db') as db: # Updates user's role when they use $profile
            cursor = db.cursor()
            cursor.execute(f"SELECT brain_pills FROM users WHERE user_id = ?", (member.id,))
            brain_pills = cursor.fetchone()
            brain_pills = brain_pills[0]
            cursor.execute(f"SELECT apmulti FROM users WHERE user_id = ?", (member.id,))
            apmultiTup = cursor.fetchone()
            apmulti = apmultiTup[0]
        if arg == "brain bean":
            if brain_pills >= 1:
                if apmulti == None or apmulti + 86400 <= timestamp:
                    sql = "UPDATE users SET apmulti = ?, brain_pills = ? WHERE user_id = ?"
                    val = (timestamp, brain_pills - 1, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(description=f"You have a 2x ap multiplier for the next 24 hours.", colour=0x800080)
                    embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(description=f"You already have a 2x multiplier.", colour=0x800080)
                    embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description=f"You need to have brain beans first!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description=f"That's not an option!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Purchase items")
    async def shop(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(title="**Item Shop**", description="You can purchase items in the shop with party points (PP)", color=0x800080)
        embed.set_author(name=(f"{member.nick}"), icon_url=member.display_avatar)
        embed.add_field(name="Brain bean (10PP)", value="A magical fruit, the more you eat the more ap you get", inline=False)
        embed.add_field(name="Impurity (5PP)", value="Smear a users name in the ultimate color of shame", inline=False)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Open your inventory")
    async def inventory(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(description=f"test")
        embed.set_author(name=(f"{member.nick}'s inventory"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    print("Items Cog Ready")
    await bot.add_cog(Item(bot), guilds=[discord.Object(id=725164114506285066)])