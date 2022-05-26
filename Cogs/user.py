import sqlite3
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="See your Essence profile!")
    async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        member_id = member.id
        timestamp = round(datetime.now().timestamp())
        command_logs = self.bot.get_channel(976519708096467025)
        spirit = discord.utils.get(
            interaction.guild.roles, id=926660576980111370)
        mana = discord.utils.get(
            interaction.guild.roles, id=926660721054462083)
        aura = discord.utils.get(
            interaction.guild.roles, id=926660747713474600)
        nature = discord.utils.get(
            interaction.guild.roles, id=928466489588191322)
        impurity = discord.utils.get(
            interaction.guild.roles, id=934956487107813426)
        party_roles = [spirit, mana, aura, nature]

        # Updates user's role when they use $profile
        with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(
                f"SELECT activity_points FROM users WHERE member_id = ?", (member_id,))
            activity_points = cursor.fetchone()
            activity_points = activity_points[0]
            cursor.execute(
                f"SELECT party_points FROM users WHERE member_id = ?", (member_id,))
            party_points = cursor.fetchone()
            party_points = party_points[0]
            cursor.execute(
                f"SELECT party_rank FROM users WHERE member_id = ?", (member_id,))
            party_rank = cursor.fetchone()
            party_rank = party_rank[0]
            cursor.execute(
                f"SELECT about FROM users WHERE member_id = ?", (member_id,))
            about = cursor.fetchone()
            about = about[0]
            cursor.execute(
                f"SELECT apmulti FROM users WHERE member_id = ?", (member_id,))
            apmulti = cursor.fetchone()
            apmulti = apmulti[0]
            cursor.execute(
                f'SELECT hide_info FROM users WHERE member_id = ?', (member.id,))
            hide_info = cursor.fetchone()
            hide_info = hide_info[0]
            cursor.execute(
                f'SELECT hide_about FROM users WHERE member_id = ?', (member.id,))
            hide_about = cursor.fetchone()
            hide_about = hide_about[0]

        no_party = 0
        for party in party_roles:
            if party in member.roles:
                party_rank = f"{party} party {party_rank}"
            else:
                no_party += 1
        if no_party == 4:
            no_party == True

        if activity_points == 0:
            desc = "This user has never sent a message, you should invite them to a conversation."
        else:
            if party_points == 0 or party_points is None:
                desc = f"They have {activity_points} A₽ in Essence!"
            else:
                desc = f"They have {activity_points} A₽ in Essence, they also have {party_points} P₽!"

        if member.nick == None:
            nickname = member.name
        else:
            nickname = member.nick

        if apmulti == None or apmulti + 86400 <= timestamp:
            apmultieffect = ""
        else:
            apmultieffect = f"\n2x A₽ until <t:{apmulti + 86400}:t>"

        if impurity in member.roles:
            impurityeffect = f"\nImpure"
        else:
            impurityeffect = ""
        effects = apmultieffect + impurityeffect

        embed = discord.Embed(
            description=desc, colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=(f"{nickname}'s Profile"),
                         icon_url=member.display_avatar)
        embed.add_field(name="Server Rank:",
                        value=member.top_role, inline=True)
        if not no_party:
            embed.add_field(name="Party Rank:", value=party_rank, inline=True)
        if not about == None and not hide_about == 1:
            embed.add_field(name=f"About:", value=about, inline=False)
        if not effects == "":
            embed.add_field(name="Effects:", value=effects, inline=False)
        if not hide_info == 1:
            embed.add_field(
                name="Info:", value=f"Joined: <t:{int(member.joined_at.timestamp())}:F>\nCreated: <t:{int(member.created_at.timestamp())}:F>\nID: {member.id}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await command_logs.send(embed=embed)

    @app_commands.command(description="Edit your profile's about me")
    async def aboutme(self, interaction: discord.Interaction, information: str = None):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        if information == None:
            with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT about FROM users WHERE member_id = ?", (member.id,))
                about = cursor.fetchone()
                about = about[0]
                if about == None:
                    embed = discord.Embed(
                        description=f"You don't have an about me yet, try making one!", colour=0x800080)
                else:
                    embed = discord.Embed(
                        description=f"**Your about me description:**\n{about}", colour=0x800080)
        else:
            if len(information) <= 256:
                if len(information.split('\n')) <= 10:
                    with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
                        cursor = db.cursor()
                    sql = "UPDATE users SET about = ? WHERE member_id = ?"
                    val = (information, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(
                        description=f"Your about me description has been updated.", colour=0x800080)
                else:
                    embed = discord.Embed(
                        description=f"Try not to have more than 10 lines of info!", colour=0x800080)
            else:
                embed = discord.Embed(
                    description=f"Your about me is too long, try shortening it to 256 characters.", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"),
                         icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await command_logs.send(embed=embed)


async def setup(bot: commands.Bot):
    print("User Cog Ready")
    await bot.add_cog(User(bot), guilds=[discord.Object(id=725164114506285066)])
