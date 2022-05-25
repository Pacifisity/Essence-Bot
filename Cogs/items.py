from xmlrpc.client import Boolean
import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Item(commands.Cog, app_commands.Group):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Allows you to use an item.")
    async def use(self, interaction: discord.Interaction, item: str):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        embed = discord.Embed(description=f"This command is a work in progress")
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

    @app_commands.command(description="Allows you to purchase items.")
    async def shop(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user

        embed = discord.Embed(title="**Item Shop**", description="You can purchase items in the shop with party points (PP)", color=0x800080)
        embed.set_author(name=(f"{member.nick}"), icon_url=member.display_avatar)
        embed.add_field(name="Brain Bean - 10 PP", value="A magical fruit, the more you eat the more ap you get", inline=False)
        embed.add_field(name="Impurity Orb - 5 PP", value="Smear a users name in the ultimate color of shame", inline=False)
        #embed.add_field(name="Custom Role - 100 PP", value="Your very own custom role, choose from currently existing custom roles or create your own.")

        select = discord.ui.Select(
            options=[
            discord.SelectOption(label="Brain Bean - 10 PP", description="A magical fruit, the more you eat the more ap you get."),
            discord.SelectOption(label="Impurity Orb - 5 PP", description="Smear a users name in the ultimate color of shame."),
            ]
        )

        async def user_response(interaction: discord.Interaction):
            embed = discord.Embed(description=f"**Purchase**", color=0x800080)
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
                cursor.execute(f"SELECT party_points FROM users WHERE member_id = ?", (member.id,))
                party_points = cursor.fetchone(); party_points = party_points[0]
                cursor.execute(f"SELECT brain_bean FROM users WHERE member_id = ?", (member.id,))
                brain_bean = cursor.fetchone(); brain_bean = brain_bean[0]
                if brain_bean == None:
                    brain_bean = 0
                cursor.execute(f"SELECT impurity_orb FROM users WHERE member_id = ?", (member.id,))
                impurity_orb = cursor.fetchone(); impurity_orb = impurity_orb[0]
                if impurity_orb == None:
                    impurity_orb = 0

            if select.values[0] == "Brain Bean - 10 PP":
                if party_points >= 10:
                    party_points = party_points - 10
                    brain_bean = brain_bean + 1
                    sql = "UPDATE users SET party_points = ?, brain_bean = ? WHERE member_id = ?"
                    val = (party_points, brain_bean, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed.add_field(name=f"-", value=f"<@{member.id}> bought `{select.values[0]}`")
                else:
                    embed.add_field(name="-", value=f"{member.nick} doesn't have enough PP to buy {select.values[0]}")

            if select.values[0] == "Impurity Orb - 5 PP":
                if party_points >= 5:
                    party_points = party_points - 5
                    impurity_orb = impurity_orb + 1
                    sql = "UPDATE users SET party_points = ?, impurity_orb = ? WHERE member_id = ?"
                    val = (party_points, impurity_orb, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed.add_field(name=f"-", value=f"<@{member.id}> bought `{select.values[0]}`")
                else:
                    embed.add_field(name="-", value=f"{member.nick} doesn't have enough PP to buy {select.values[0]}")

            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
        
        select.callback = user_response
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True); await command_logs.send(embed=embed, view=view)
    
    @app_commands.command(description="Shows a list of all of your items.")
    async def inventory(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        embed = discord.Embed(description=f"**Inventory**", colour=0x800080)
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT brain_bean, crystal_of_power, joker_card, easter_egg, impurity_orb FROM users WHERE member_id = ?", (member.id,))
            inventory = cursor.fetchone()
            items = ["Brain Bean", "Crystal of Power", "Joker Card", "Easter Egg", "Impurity Orb"]
            for i in enumerate(inventory):
                if not i[1] == None:
                    embed.add_field(name=f"{items[i[0]]}:", value=f"{i[1]}", inline=False)
            embed.set_author(name=(f"{member.nick}'s Command:"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

async def setup(bot: commands.Bot):
    print("Items Cog Ready")
    await bot.add_cog(Item(bot), guilds=[discord.Object(id=725164114506285066)])