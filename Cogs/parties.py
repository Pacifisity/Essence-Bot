import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import random

class Party(commands.Cog, app_commands.Group):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
        
    async def cog_check(self, ctx):
        channel1, channel2, channel3 = self.bot.get_channel(735131468145360917), self.bot.get_channel(920479737405644830), self.bot.get_channel(927583858856177694)
        return ctx.channel == channel1 or ctx.channel == channel2 or ctx.channel == channel3

    @app_commands.command(description="Get party information")
    async def info(self, interaction: discord.Interaction, arg: str = None):
        member = interaction.user
        arg = str.lower(arg)
        command_logs = self.bot.get_channel(976519708096467025)

        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party, SUM(party_points) FROM users GROUP BY party")
            party_total = cursor.fetchall()
            cursor.execute(f"SELECT essence_points FROM server WHERE party = ?", (arg,))
            essence_points = cursor.fetchone()

        if arg == 'spirit':
            embed = discord.Embed(title="Party Spirit", description="Party led by <@491289245974003722>, those who join party spirit want to become one with Essence energy. ($party spirit)",  colour=0x800080)
            embed.add_field(name="Party Spirit Points:", value=f"{party_total[4][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

        elif arg == "mana":
            embed = discord.Embed(title="Party Mana", description="Party led by <@261900816841965570>, those who join party mana want to take control of Essence energy. ($party mana)",  colour=0xd6680e)
            embed.add_field(name="Party Mana Points:", value=f"{party_total[2][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

        elif arg == "aura":
            embed = discord.Embed(title="Party Aura", description="Party led by <@508504220354347018>, those who join party aura want to use Essence energy as an external power. ($party aura)",  colour=0xca0a0a)
            embed.add_field(name="Party Aura Points:", value=f"{party_total[1][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

        elif arg == "nature":
            embed = discord.Embed(title="Party Nature", description="Those who join the nature party want essence to be left in it's base form, unmanipulated and naturally flowing. ($party nature)",  colour=0x00ff00)
            embed.add_field(name="Party Nature Points:", value=f"{party_total[3][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
        
        else:
            embed = discord.Embed(title="Parties", description=f"Parties are teams, party **spirit**, party **mana**, party **aura** and party **nature**. Each party is competing against the other party for party points (₽₽) and essence points (TBD). These points will be used in leaderboards and as a currency for a shop in the coming future. Events can be from 3v3v3v3 battle royales to a pet picture competition :wink:!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

    @app_commands.command(description="Join a party!")
    async def join(self, interaction: discord.Interaction, party: str or None):
        member = interaction.user
        arg = str.lower(arg)
        command_logs = self.bot.get_channel(976519708096467025)
        Spirit = discord.utils.get(interaction.guild.roles, id=926660576980111370) 
        Mana = discord.utils.get(interaction.guild.roles, id=926660721054462083) 
        Aura = discord.utils.get(interaction.guild.roles, id=926660747713474600) 
        Nature = discord.utils.get(interaction.guild.roles, id=928466489588191322)

        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party FROM users WHERE user_id = ?", (member.id,))
            party = cursor.fetchone()
            party = party[0]
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member.id,))
            party_points = cursor.fetchone()
            party_points = party_points[0]

        if party == None:
            if arg == "spirit":
                sql = "UPDATE users SET party_points = ?, party = ?, party_rank = ? WHERE user_id = ?"
                if party_points == None or party_points >= 10:
                    val = (10, 'Spirit', 'Recruit', member.id)
                else:
                    val = (party_points, 'Spirit', 'Recruit', member.id)
                cursor.execute(sql, val)
                db.commit()
                await member.add_roles(Spirit)
                embed = discord.Embed(description=f"Welcome to party Spirit!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

            elif arg == "mana":
                sql = "UPDATE users SET party_points = ?, party = ?, party_rank = ? WHERE user_id = ?"
                if party_points == None or party_points >= 10:
                    val = (10, 'Mana', 'Recruit', member.id)
                else:
                    val = (party_points, 'Mana', 'Recruit', member.id)
                cursor.execute(sql, val)
                db.commit()
                await member.add_roles(Mana)
                embed = discord.Embed(description=f"Welcome to party Mana!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

            elif arg == "aura":
                sql = "UPDATE users SET party_points = ?, party = ?, party_rank = ? WHERE user_id = ?"
                if party_points == None or party_points >= 10:
                    val = (10, 'Aura', 'Recruit', member.id)
                else:
                    val = (party_points, 'Aura', 'Recruit', member.id)
                cursor.execute(sql, val)
                db.commit()
                await member.add_roles(Aura)
                embed = discord.Embed(description=f"Welcome to party Aura!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

            elif arg == "nature":
                sql = "UPDATE users SET party_points = ?, party = ?, party_rank = ? WHERE user_id = ?"
                if party_points == None or party_points >= 10:
                    val = (10, 'Nature', 'Recruit', member.id)
                else:
                    val = (party_points, 'Nature', 'Recruit', member.id)
                cursor.execute(sql, val)
                db.commit()
                await member.add_roles(Nature)
                embed = discord.Embed(description=f"Welcome to party Nature!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

            else:
                embed = discord.Embed(title="Parties", description=f"Which party would you like to join?\n\nParties are teams, party **spirit**, party **mana**, party **aura** and party **nature**. Each party is competing against the other party for party points (₽₽) and essence points (TBD). These points will be used in leaderboards and as a currency for a shop in the coming future. Events can be from 3v3v3v3 battle royales to a pet picture competition :wink:!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
        else:
            embed = discord.Embed(title="Parties", description=f"You are already in a party", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

    @app_commands.command(description="Leave a party")
    async def leave(self, interaction: discord.Interaction, arg: str or None):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        arg = str.lower(arg)
        Spirit = discord.utils.get(interaction.guild.roles, id=926660576980111370) 
        Mana = discord.utils.get(interaction.guild.roles, id=926660721054462083) 
        Aura = discord.utils.get(interaction.guild.roles, id=926660747713474600) 
        Nature = discord.utils.get(interaction.guild.roles, id=928466489588191322)

        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party FROM users WHERE user_id = ?", (member.id,))
            party = cursor.fetchone()
            party = party[0]
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member.id,))
            party_points = cursor.fetchone()
            party_points = party_points[0]
        if arg == "confirm":
            if party == None:
                    embed = discord.Embed(description=f"You're not in a party.", colour=0x800080)
                    embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                    await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
            else:
                if party_points < 10:
                    pp = party_points
                    await member.remove_roles(Spirit)
                    await member.remove_roles(Mana)
                    await member.remove_roles(Aura)
                    await member.remove_roles(Nature)
                    sql = "UPDATE users SET party = ?, pp_storage = ?, party_points = ?, party_rank = ? WHERE user_id = ?"
                    val = (None, pp, None, None, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(description=f"You have left your party.", colour=0x800080)
                    embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                    await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
                else:
                    await member.remove_roles(Spirit)
                    await member.remove_roles(Mana)
                    await member.remove_roles(Aura)
                    await member.remove_roles(Nature)
                    sql = "UPDATE users SET party = ?, party_points = ?, party_rank = ? WHERE user_id = ?"
                    val = (None, None, None, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(description=f"You have left your party.", colour=0x800080)
                    embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                    await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
        else:
            embed = discord.Embed(title="Are you sure you want to leave your party?", description="If you are sure you want to leave your party do /party leave confirm\n\nIf you leave your party, you will lose you party rank and any extra party points. Spend all party points above 10 before you leave your party.",  colour=0x00ff00)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
    
    @app_commands.command(description="Collect your daily party point")
    async def daily(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        impurity = discord.utils.get(interaction.guild.roles, id=934956487107813426) 
        timestamp = round(datetime.now().timestamp())
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member.id,))
            party_points = cursor.fetchone(); party_points = party_points[0]
            cursor.execute(f"SELECT party FROM users WHERE user_id = ?", (member.id,))
            party = cursor.fetchone(); party = party[0]
            cursor.execute(f"SELECT brain_bean FROM users WHERE user_id = ?", (member.id,))
            brain_bean = cursor.fetchone(); brain_bean = brain_bean[0]
            if brain_bean == None:
                brain_bean = 0
            cursor.execute(f"SELECT daily FROM users WHERE user_id = ?", (member.id,))
            daily_cooldown = cursor.fetchone(); daily_cooldown = daily_cooldown[0]
            if daily_cooldown == None:
                daily_cooldown = 0
            
        if party == None:
            embed = discord.Embed(description=f"You have to join a party first!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
            return

        if daily_cooldown >= (timestamp - 86400):
            embed = discord.Embed(description=f"You can claim your daily <t:{daily_cooldown + 86400}:R> (<t:{daily_cooldown + 86400}:t>)", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
            return

        if not daily_cooldown >= (timestamp - 86400):
            embed = discord.Embed(description=f"Daily point claimed!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            pill = random.randint(1,10)
            party_points += 1
            sql = "UPDATE users SET party_points = ?, daily = ?, daily_reminder = ? WHERE user_id = ?"
            val = (party_points, timestamp, 1, member.id)
            cursor.execute(sql, val)
            db.commit()
            if pill == 1:
                embed.add_field(name='-', value="You've gained a brain bean!")
                sql = "UPDATE users SET brain_bean = ? WHERE user_id = ?"
                val = (brain_bean + 1, member.id)
                cursor.execute(sql, val)
                db.commit()
            
        if impurity in member.roles:
            embed.add_field(value="You've been cleansed from your impurity")
            await member.remove_roles(impurity)

        await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

async def setup(bot: commands.Bot):
    print("Party Cog Ready")
    await bot.add_cog(Party(bot), guilds=[discord.Object(id=725164114506285066)])