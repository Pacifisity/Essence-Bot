import sqlite3
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="See your Essence profile!")
    async def profile(self, interaction: discord.Interaction, arg: discord.Member = None):
        if arg == None:
            member = interaction.user
        else:
            member = arg
        member_id = member.id
        timestamp = round(datetime.now().timestamp())
        guild_roles = [
        discord.utils.get(interaction.guild.roles, id=(867097611323310082)), # Visitor 0
        discord.utils.get(interaction.guild.roles, id=(730626889709781043)), # Guest 1
        discord.utils.get(interaction.guild.roles, id=(795491852533891112)), # Member 2
        discord.utils.get(interaction.guild.roles, id=(865644597140258827)), # Honorary Member 3
        discord.utils.get(interaction.guild.roles, id=(865644927114412073)), # VIP 4
        discord.utils.get(interaction.guild.roles, id=(741152373921022092)), # Moderator 5
        discord.utils.get(interaction.guild.roles, id=(795441220885151784)), # Administrator 6
        discord.utils.get(interaction.guild.roles, id=(734838525144596493)), # Robot 7
        discord.utils.get(interaction.guild.roles, id=(926660576980111370)), # Spirit 8
        discord.utils.get(interaction.guild.roles, id=(926660721054462083)), # Mana 9
        discord.utils.get(interaction.guild.roles, id=(926660747713474600)), # Aura 10
        discord.utils.get(interaction.guild.roles, id=(928466489588191322)), # Nature 11
        discord.utils.get(interaction.guild.roles, id=(934956487107813426))] # Impurity 12
        Visitor = guild_roles[0]
        Guest = guild_roles[1]
        Member = guild_roles[2]
        HonoraryMember = guild_roles[3]
        VIP = guild_roles[4]
        Moderator = guild_roles[5]
        Administrator = guild_roles[6]
        Robot = guild_roles[7]
        Spirit = guild_roles[8]
        Mana = guild_roles[9]
        Aura = guild_roles[10]
        Nature = guild_roles[11]
        Impurity = guild_roles[12]
        with sqlite3.connect('DB Storage/essence.db') as db: # Updates user's role when they use $profile
            cursor = db.cursor()
            cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (member_id,))
            messages = cursor.fetchone()
            if messages == None:
                messages = 0
            else:
                messages = messages[0]
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member_id,))
            partyPoints = cursor.fetchone()
            if not partyPoints == None:
                partyPoints = partyPoints[0]
            cursor.execute(f"SELECT party_rank FROM users WHERE user_id = ?", (member_id,))
            partyRank = cursor.fetchone()
            cursor.execute(f"SELECT about FROM users WHERE user_id = ?", (member_id,))
            about = cursor.fetchone()
            if about == None:
                pass
            else:
                about = about[0]
            cursor.execute(f"SELECT apmulti FROM users WHERE user_id = ?", (member_id,))
            apmulti = cursor.fetchone()
            if apmulti == None:
                pass
            else:
                apmulti = apmulti[0]
        if Spirit in member.roles:
            pRank=f"{Spirit} Party {partyRank[0]}"
        elif Mana in member.roles:
            pRank=f"{Mana} Party {partyRank[0]}"
        elif Aura in member.roles:
            pRank=f"{Aura} Party {partyRank[0]}"
        elif Nature in member.roles:
            pRank=f"{Nature} Party {partyRank[0]}"
        else:
            if arg == None:
                pRank="You are not in a party!"
            else:
                pRank="They are not in a party!"
        if 100 - messages < 0:
            GAP = ""
        else:
            GAP = f"{100 - messages} A₽"
        if 1000 - messages < 0:
            MAP = ""
        else:
            MAP = f"{1000 - messages} A₽"
        if 10000 - messages < 0:
            HMAP = ""
            if partyPoints is None:
                HMPP = f" and 25 P₽"
            elif partyPoints < 25:
                HMPP = f" and {25 - partyPoints} P₽"
            else:
                HMPP = ""
        else:
            HMAP = f"{10000 - messages} A₽"
            if partyPoints is None:
                HMPP = f" and 25 P₽"
            elif partyPoints < 25:
                HMPP = f" and {25 - partyPoints} P₽"
            else:
                HMPP = ""
        if 100000 - messages < 0:
            VAP = ""
            if partyPoints is None:
                VPP = f" and 100 P₽"
            elif partyPoints < 100:
                VPP = f" and {100 - partyPoints} P₽"
            else:
                VPP = ""
        else:
            VAP = f"{100000 - messages} A₽"
            if partyPoints is None:
                VPP = f" 100 P₽"
            elif partyPoints < 100:
                VPP = f" and {100 - partyPoints} P₽"
            else:
                VPP = ""
        if messages is None: # New user (Visitor role)
            if Guest in member.roles:
                Reward = f"{MAP} away from becoming a Member."
            elif Member in member.roles:
                Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
            elif HonoraryMember in member.roles:
                Reward = f"{VAP}{VPP} away from becoming a VIP."
            elif VIP in member.roles:
                Reward = f"No further rewards to unlock"
            elif Moderator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Administrator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Robot in member.roles:
                Reward = f"No further rewards to unlock"
            else:
                Reward = "100 A₽ away from becoming a Guest."
        if messages < 100: # New user (Visitor role)
            if Guest in member.roles:
                Reward = f"{MAP} away from becoming a Member."
            elif Member in member.roles:
                Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
            elif HonoraryMember in member.roles:
                Reward = f"{VAP}{VPP} away from becoming a VIP."
            elif VIP in member.roles:
                Reward = f"No further rewards to unlock"
            elif Moderator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Administrator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Robot in member.roles:
                Reward = f"No further rewards to unlock"
            else:
                Reward = f"{GAP} away from becoming a Guest."
        if messages >= 100: # Guest
            if Guest in member.roles:
                Reward = f"{MAP} away from becoming a Member."
            elif Member in member.roles:
                Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
            elif HonoraryMember in member.roles:
                Reward = f"{VAP}{VPP} away from becoming a VIP."
            elif VIP in member.roles:
                Reward = f"No further rewards to unlock"
            elif Moderator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Administrator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Robot in member.roles:
                Reward = f"No further rewards to unlock"
            else:
                await member.remove_roles(Visitor)
                await member.add_roles(Guest)
                Reward = f"You just became a Guest"
        if messages >= 1000: # Member
            if Member in member.roles:
                Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
            elif HonoraryMember in member.roles:
                Reward = f"{VAP}{VPP} away from becoming a VIP."
            elif VIP in member.roles:
                Reward = f"No further rewards to unlock"
            elif Moderator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Administrator in member.roles:
                Reward = f"No further rewards to unlock"
            elif Robot in member.roles:
                Reward = f"No further rewards to unlock"
            else:
                await member.remove_roles(Guest)
                await member.add_roles(Member)
                Reward = f"You just became a Member"
        if messages >= 10000: # HonoraryMember
            if partyPoints is None:
                if Member in member.roles:
                    Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
                elif HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    Reward = f"{HMPP} away from becoming a Honorary Member"
            elif partyPoints >= 25:
                if Member in member.roles:
                    Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
                elif HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    await member.remove_roles(Member)
                    await member.add_roles(HonoraryMember)
                    Reward = f"You just became an Honorary Member"
            else:
                if Member in member.roles:
                    Reward = f"{HMAP}{HMPP} away from becoming an Honorary Member."
                elif HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    Reward = f"{HMPP} away from becoming a Honorary Member"
        if messages >= 100000: # VIP
            if partyPoints is None:
                if HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    Reward = f"{VPP} away from becoming a VIP"
            elif partyPoints >= 100:
                if HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    await member.remove_roles(HonoraryMember)
                    await member.add_roles(VIP)
                    Reward = f"You just became a VIP"
            else:
                if HonoraryMember in member.roles:
                    Reward = f"{VAP}{VPP} away from becoming a VIP."
                elif VIP in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Moderator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Administrator in member.roles:
                    Reward = f"No further rewards to unlock"
                elif Robot in member.roles:
                    Reward = f"No further rewards to unlock"
                else:
                    Reward = f"{VPP} away from becoming a VIP"
                    
        if Visitor in member.roles:
            sRank=Visitor
        elif Guest in member.roles:
            sRank=Guest
        elif Member in member.roles:
            sRank=Member
        elif HonoraryMember in member.roles:
            sRank=HonoraryMember
        elif VIP in member.roles:
            sRank=VIP
        elif Moderator in member.roles:
            sRank=Moderator
        elif Administrator in member.roles:
            sRank=Administrator
        elif Robot in member.roles:
            sRank=Robot

        if arg == None:
            if messages == 0:
                desc = "This user has never sent a message, you should invite them to a conversation."
            else:
                if partyPoints == 0 or partyPoints is None:
                    desc = f"You have {messages} A₽ in Essence!"
                else:
                    desc = f"You have {messages} A₽ in Essence, you also have {partyPoints} P₽!"
        else:
            if messages == 0:
                desc = "This user has never sent a message, you should invite them to a conversation."
            else:
                if partyPoints == 0 or partyPoints is None:
                    desc = f"They have {messages} A₽ in Essence!"
                else:
                    desc = f"They have {messages} A₽ in Essence, they also have {partyPoints} P₽!"

        if member.nick == None:
            nickname = member.name
        else:
            nickname = member.nick

        if apmulti == None or apmulti + 86400 <= timestamp:
            apmultieffect = ""
        else:
            apmultieffect = f"\n2x A₽ until <t:{apmulti + 86400}:t>"

        if Impurity in member.roles:
            impurityeffect = f"\nImpure"
        else:
            impurityeffect = ""
        effects = apmultieffect + impurityeffect
            
        embed = discord.Embed(description=desc, colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=(f"{nickname}'s Profile"), icon_url=member.display_avatar)
        embed.add_field(name="Server Rank", value=sRank, inline=True)
        embed.add_field(name="Party Rank", value=pRank, inline=True)
        if not about == None:
            embed.add_field(name=f"About {nickname}", value=about, inline=False)
        else:
            embed.add_field(name=f"About {nickname}", value="Tell us a bit about yourself with /aboutme!", inline=False)
        if not effects == "":
            embed.add_field(name="Effects", value=effects, inline=False)
        embed.add_field(name="Next Reward", value=Reward, inline=False)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Edit your profile's about me")
    async def aboutme(self, interaction: discord.Interaction, *, arg: str or None):
        if len(arg) <= 256:
            if len(arg.split('\n')) < 11:
                member = interaction.user
                with sqlite3.connect('DB Storage/essence.db') as db:
                    cursor = db.cursor()
                sql = "UPDATE users SET about = ? WHERE user_id = ?"
                val = (arg, member.id)
                cursor.execute(sql, val)
                db.commit()
                embed = discord.Embed(description=f"Your about me description has been updated.", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description=f"Try not to have more than 10 lines of info!", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description=f"Your about me is too long, try shortening it to 256 characters.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    print("User Cog Ready")
    await bot.add_cog(User(bot), guilds=[discord.Object(id=725164114506285066)])