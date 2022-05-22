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
        guild_roles = [
        discord.utils.get(interaction.guild.roles, id=(867097611323310082)), # visitor 0
        discord.utils.get(interaction.guild.roles, id=(730626889709781043)), # guest 1
        discord.utils.get(interaction.guild.roles, id=(795491852533891112)), # member 2
        discord.utils.get(interaction.guild.roles, id=(865644597140258827)), # Honorary member 3
        discord.utils.get(interaction.guild.roles, id=(865644927114412073)), # vip 4
        discord.utils.get(interaction.guild.roles, id=(741152373921022092)), # mod 5
        discord.utils.get(interaction.guild.roles, id=(795441220885151784)), # admin 6
        discord.utils.get(interaction.guild.roles, id=(734838525144596493)), # robot 7
        discord.utils.get(interaction.guild.roles, id=(926660576980111370)), # spirit 8
        discord.utils.get(interaction.guild.roles, id=(926660721054462083)), # mana 9
        discord.utils.get(interaction.guild.roles, id=(926660747713474600)), # aura 10
        discord.utils.get(interaction.guild.roles, id=(928466489588191322)), # nature 11
        discord.utils.get(interaction.guild.roles, id=(934956487107813426))] # impurity 12
        visitor = guild_roles[0]
        guest = guild_roles[1]
        member_role = guild_roles[2]
        honorary_member = guild_roles[3]
        vip = guild_roles[4]
        mod = guild_roles[5]
        admin = guild_roles[6]
        robot = guild_roles[7]
        spirit = guild_roles[8]
        mana = guild_roles[9]
        aura = guild_roles[10]
        nature = guild_roles[11]
        impurity = guild_roles[12]
        attainable_roles = [visitor, guest, member_role, honorary_member, vip]
        party_roles = [spirit, mana, aura, nature]

        with sqlite3.connect('DB Storage/essence.db') as db: # Updates user's role when they use $profile
            cursor = db.cursor()
            cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (member_id,))
            activity_points = cursor.fetchone(); activity_points = activity_points[0]
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member_id,))
            party_points = cursor.fetchone(); party_points = party_points[0]
            cursor.execute(f"SELECT party_rank FROM users WHERE user_id = ?", (member_id,))
            party_rank = cursor.fetchone(); party_rank = party_rank[0]
            cursor.execute(f"SELECT about FROM users WHERE user_id = ?", (member_id,))
            about = cursor.fetchone(); about = about[0]
            cursor.execute(f"SELECT apmulti FROM users WHERE user_id = ?", (member_id,))
            apmulti = cursor.fetchone(); apmulti = apmulti[0]

        for party in party_roles:
            if party in member.roles:
                party_rank = f"{party} party {party_rank}"
                party_check = 1
        if party_check != 1:
            party_rank = None

        if activity_points >= 100000 and party_points >= 100: # vip
            if vip or mod or admin in member.roles:
                Reward = None
            else:
                member.add_roles(vip)
                for role in attainable_roles:
                    if role in member.roles:
                        member.remove_roles(role)

        elif activity_points >= 10000 and party_points >= 25: # Honorary member
            if vip or mod or admin in member.roles:
                Reward = None
            elif honorary_member in member.roles:
                Reward = f"{100000 - activity_points} more activity points and {100 - party_points} party points to unlock the next role!"
            else:
                member.add_roles(honorary_member)
                for role in attainable_roles:
                    if role in member.roles:
                        member.remove_roles(role)

        elif activity_points >= 1000: # member
            if honorary_member or vip or mod or admin in member.roles:
                Reward = None
            elif member_role in member.roles:
                Reward = f"{10000 - activity_points} more activity points and {25 - party_points} party points to unlock the next role!"
            else:
                member.add_roles(member_role)
                for role in attainable_roles:
                    if role in member.roles:
                        member.remove_roles(role)

        elif activity_points >= 100: # guest
            if member_role or honorary_member or vip or mod or admin in member.roles:
                Reward = None
            elif guest in member.roles:
                Reward = f"{1000 - activity_points} more activity points to unlock the next role!"
            else:
                member.add_roles(guest)
                for role in attainable_roles:
                    if role in member.roles:
                        member.remove_roles(role)

        elif activity_points >= 0: # visitor
            if guest or member_role or honorary_member or vip or mod or admin in member.roles:
                Reward = None
            elif visitor in member.roles:
                Reward = f"{100 - activity_points} more activity points to unlock the next role!"
            else:
                member.add_roles(visitor)
                for role in attainable_roles:
                    if role in member.roles:
                        member.remove_roles(role)
                        
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
            
        embed = discord.Embed(description=desc, colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=(f"{nickname}'s Profile"), icon_url=member.display_avatar)
        embed.add_field(name="Server Rank:", value=member.top_role, inline=True)
        if not party_rank == None:
            embed.add_field(name="Party Rank:", value=party_rank , inline=True)
        if not about == None:
            embed.add_field(name=f"About:", value=about, inline=False)
        if not effects == "":
            embed.add_field(name="Effects:", value=effects, inline=False)
        if not Reward == None:
            embed.add_field(name="Next Reward:", value=Reward, inline=False)
        embed.add_field(name="Info:", value=f"Joined: <t:{int(member.joined_at.timestamp())}:t>\nCreated: <t:{int(member.created_at.timestamp())}:t>\nID: {member.id}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)
    
    @app_commands.command(description="Edit your profile's about me")
    async def aboutme(self, interaction: discord.Interaction, *, member: str or None):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        if len(member) <= 256:
            if len(member.split('\n')) < 11:
                with sqlite3.connect('DB Storage/essence.db') as db:
                    cursor = db.cursor()
                sql = "UPDATE users SET about = ? WHERE user_id = ?"
                val = (member, member.id)
                cursor.execute(sql, val)
                db.commit()
                embed = discord.Embed(description=f"Your about me description has been updated.", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            else:
                embed = discord.Embed(description=f"Try not to have more than 10 lines of info!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        else:
            embed = discord.Embed(description=f"Your about me is too long, try shortening it to 256 characters.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await command_logs.send(embed=embed)

async def setup(bot: commands.Bot):
    print("User Cog Ready")
    await bot.add_cog(User(bot), guilds=[discord.Object(id=725164114506285066)])