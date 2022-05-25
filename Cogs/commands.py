import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime

mod = 741152373921022092

class Essence(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.command_logs = self.bot.get_channel(976519708096467025)
    
    """
    @app_commands.command(description="Write a note you can pull up at any time")
    async def note(self, interaction: discord.Interaction, options: str, note: str):
        member = interaction.user
        note_check = note.count('@')
        if not note_check > 0:
            print(note)
        else:
            print("Pain, don't try that")
    """
    
    @app_commands.command(description="Hide information from your profile")
    async def hide(self, interaction: discord.Interaction, options: str = None):
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT hide_info FROM users WHERE member_id = ?', (member.id,))
            hide_info = cursor.fetchone(); hide_info = hide_info[0]
            cursor.execute(f'SELECT hide_about FROM users WHERE member_id = ?', (member.id,))
            hide_about = cursor.fetchone(); hide_about = hide_about[0]
            if options == None:
                embed = discord.Embed(description=f"about = Your about me section\ninfo = Your account information section", colour=0x800080)
            elif options == 'about':
                if hide_about == None or hide_about == 0:
                    sql = "UPDATE users SET hide_about = ? WHERE member_id = ?"
                    val = (1, member.id)
                    embed = discord.Embed(description=f"You have hidden your about section.", colour=0x800080)
                else:
                    sql = "UPDATE users SET hide_about = ? WHERE member_id = ?"
                    val = (0, member.id)
                    embed = discord.Embed(description=f"Your about section is visible now.", colour=0x800080)

            elif options == 'info':
                if hide_info == None or hide_info == 0:
                    sql = "UPDATE users SET hide_info = ? WHERE member_id = ?"
                    val = (1, member.id)
                    embed = discord.Embed(description=f"You have hidden your info.", colour=0x800080)
                else:
                    sql = "UPDATE users SET hide_info = ? WHERE member_id = ?"
                    val = (0, member.id)
                    embed = discord.Embed(description=f"Your info is visible now.", colour=0x800080)

                cursor.execute(sql, val)
                db.commit()
            else:
                embed = discord.Embed(description=f"about = Your about me section\ninfo = Your account information section", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)

    # Auto role commands -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @app_commands.command(description="Toggles notifications across Essence")
    async def notifications(self, interaction: discord.Interaction):
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT notifications FROM users WHERE member_id = ?', (member.id,))
            notifications = cursor.fetchone(); notifications = notifications[0]
            if notifications == None or notifications == 0:
                sql = "UPDATE users SET notifications = ? WHERE member_id = ?"
                val = (1, member.id)
                embed = discord.Embed(description=f"You have been signed up for notifications across Essence, if you ignore a notification it will not come up again.", colour=0x800080)
            else:
                sql = "UPDATE users SET notifications = ? WHERE member_id = ?"
                val = (0, member.id)
                embed = discord.Embed(description=f"You have turned off notifications across Essence.", colour=0x800080)
            cursor.execute(sql, val)
            db.commit()
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)
    
    @app_commands.command(description="Gives you the artist role and access to talk in the art channel")
    async def artist(self, interaction: discord.Interaction):
        member = interaction.user
        artist = discord.utils.get(interaction.guild.roles, id=758084699007746179)
        await member.add_roles(artist)
        embed = discord.Embed(description=f"You have been given the artist role, remember to follow the channel topics and look at pins to keep it clean.", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)
    
    @app_commands.command(description="Gives you the supporter role and access to the entertainment category")
    async def supporter(self, interaction: discord.Interaction):
        member = interaction.user
        supporter = discord.utils.get(interaction.guild.roles, id=741720677308039278)
        await member.add_roles(supporter)
        embed = discord.Embed(description=f"You have been given the supporter role, access to entertainment channels has been given", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)

    @app_commands.command(description="Changes your nickname based on the format 'Nick - Username'")
    async def nick(self, interaction: discord.Interaction, arg: str = None):
        member = interaction.user
        await member.edit(nick=f"{arg} - {member.name}")
        embed = discord.Embed(description=f"Your nickname has been updated, {member.mention}", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)

    @app_commands.command(description="Josh's character description.")
    @app_commands.checks.has_role(mod)
    async def josh(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(description=f"https://clips.twitch.tv/SpoopyTallNightingaleHeyGuys It all started when I was a wee lad.  I was an avid evil hunter at the time, so whenever I came across anyone with an evil reputation, I hunted them. It was on one such fine evening that I found my quarry. A certain Bill Gates. After I killed him he respawned and came after me, but with backup. I did my best but alas, I could not 1v2, so I retreated into the forest, all the while taunting in chat. I thought I had earned a well-deserved respite, but only a few moments later the tree I was standing in disintegrated. They had found me. So I ran. I am unsure of what happened during this time, but a bit after my escape into the forest, one of the friends of Bill Gates sent me a message I think. I really don't know how it happened but I was somehow pulled into Discord with a man named Crystal. One thing led to another and I got roped into the guild called Acquisitive.” ~Josh", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)
    
    @app_commands.command(description="Make a suggestion!")
    async def suggest(self, interaction: discord.Interaction, suggestion: str = None):
        member = interaction.user
        if suggestion == None:
            embed = discord.Embed(description=f"There seems to be a problem with your suggestion, {member}!", colour=0x800080)
        else:
            channel = self.bot.get_channel(927368289821294612)
            embed = discord.Embed(description=f"{suggestion} suggested by <@{member.id}>", colour=0x800080)
            await channel.send(embed=embed)
            embed = discord.Embed(description=f"Your suggestion has been sent to the organizer.", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)
    
    @app_commands.command(description="Get the bot latency")
    async def ping(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(description=f"Pong! {round(self.bot.latency * 1000)}ms", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)

    @app_commands.command(description="Set the bot's status")
    async def setstatus(self, interaction: discord.Interaction, *, status: str):
        member = interaction.user
        party = 'spirit'
        if len(status) <= 128:
            await self.bot.change_presence(activity=discord.Game(name=status))
            embed = discord.Embed(description="Bot status set to `Playing " + str(status) + "`", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE server SET status = ? WHERE party = ?"
                val = (status, party)
                cursor.execute(sql, val)
                db.commit()
        else:
            embed = discord.Embed(description=f"Too many characters, the bot's status can't support more than 128 characters.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)
    
    @app_commands.command(description="Look at the different leaderboards")
    async def leaderboard(self, interaction: discord.Interaction, board: str = None):
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            if board == None:
                embed = discord.Embed(title="Leaderboard Ranking", colour=0x800080)
                for ranking in ["activity_points", "party_points", "user_count"]:
                    cursor.execute(f"SELECT member_id FROM users ORDER BY {ranking} DESC")
                    leaderboard = cursor.fetchall()
                    for i, (member_id,) in enumerate(leaderboard, start=1):
                        if member_id == member.id:
                            if ranking == "activity_points":
                                ranking = "Activity Points Rank:"
                            if ranking == "party_points":
                                ranking = "Party Points Rank:"
                            if ranking == "user_count":
                                ranking = "Counting Rank:"
                            if i <= 1:
                                rank = ":first_place:"
                            elif i <= 2:
                                rank = ":second_place:"
                            elif i <= 3:
                                rank = ":third_place:"
                            elif i <= 10:
                                rank = ":medal:"
                            else:
                                rank = f"#{i}"
                            embed.add_field(name=ranking, value=rank, inline=False)
            elif board == 'pp':
                cursor.execute(f"SELECT member_id, party_points, party FROM users GROUP BY member_id ORDER BY 2 DESC LIMIT 10")
                leaderboard = cursor.fetchall()
                cursor.execute(f"SELECT party, SUM(party_points) FROM users GROUP BY party")
                leaderboard2 = cursor.fetchall()
                embed = discord.Embed(title="Party Point Leaderboard", description=f":first_place: <@{leaderboard[0][0]}> {leaderboard[0][2]} member with {leaderboard[0][1]} ₽₽!\n :second_place: <@{leaderboard[1][0]}> {leaderboard[1][2]} member with {leaderboard[1][1]} ₽₽!\n :third_place: <@{leaderboard[2][0]}> {leaderboard[2][2]} member with {leaderboard[2][1]} ₽₽!\n :medal: <@{leaderboard[3][0]}> {leaderboard[3][2]} member with {leaderboard[3][1]} ₽₽!\n :medal: <@{leaderboard[4][0]}> {leaderboard[4][2]} member with {leaderboard[4][1]} ₽₽!\n :medal: <@{leaderboard[5][0]}> {leaderboard[5][2]} member with {leaderboard[5][1]} ₽₽!\n :medal: <@{leaderboard[6][0]}> {leaderboard[6][2]} member with {leaderboard[6][1]} ₽₽!\n :medal: <@{leaderboard[7][0]}> {leaderboard[7][2]} member with {leaderboard[7][1]} ₽₽!\n :medal: <@{leaderboard[8][0]}> {leaderboard[8][2]} member with {leaderboard[8][1]} ₽₽!\n :medal: <@{leaderboard[9][0]}> {leaderboard[9][2]} member with {leaderboard[9][1]} ₽₽!", colour=0x800080, timestamp=datetime.utcnow())
                embed.add_field(name="Cumulative party points", value=f"{leaderboard2[4][0]} {leaderboard2[4][1]} ₽₽ | {leaderboard2[2][0]} {leaderboard2[2][1]} ₽₽ | {leaderboard2[1][0]} {leaderboard2[1][1]} ₽₽ | {leaderboard2[3][0]} {leaderboard2[3][1]} ₽₽")
            elif board == 'ap':
                cursor.execute(f"SELECT member_id, activity_points, party FROM users GROUP BY member_id ORDER BY 2 DESC LIMIT 10")
                leaderboard = cursor.fetchall()
                cursor.execute(f"SELECT party, SUM(activity_points) FROM users GROUP BY party")
                leaderboard2 = cursor.fetchall()
                embed = discord.Embed(title="Activity Point Leaderboard", description=f":first_place: <@{leaderboard[0][0]}> {leaderboard[0][2]} member with {leaderboard[0][1]} A₽!\n :second_place: <@{leaderboard[1][0]}> {leaderboard[1][2]} member with {leaderboard[1][1]} A₽!\n :third_place: <@{leaderboard[2][0]}> {leaderboard[2][2]} member with {leaderboard[2][1]} A₽!\n :medal: <@{leaderboard[3][0]}> {leaderboard[3][2]} member with {leaderboard[3][1]} A₽!\n :medal: <@{leaderboard[4][0]}> {leaderboard[4][2]} member with {leaderboard[4][1]} A₽!\n :medal: <@{leaderboard[5][0]}> {leaderboard[5][2]} member with {leaderboard[5][1]} A₽!\n :medal: <@{leaderboard[6][0]}> {leaderboard[6][2]} member with {leaderboard[6][1]} A₽!\n :medal: <@{leaderboard[7][0]}> {leaderboard[7][2]} member with {leaderboard[7][1]} A₽!\n :medal: <@{leaderboard[8][0]}> {leaderboard[8][2]} member with {leaderboard[8][1]} A₽!\n :medal: <@{leaderboard[9][0]}> {leaderboard[9][2]} member with {leaderboard[9][1]} A₽!", colour=0x800080, timestamp=datetime.utcnow())
                embed.add_field(name="Cumulative party points", value=f"{leaderboard2[4][0]} {leaderboard2[4][1]} A₽ | {leaderboard2[2][0]} {leaderboard2[2][1]} A₽ | {leaderboard2[1][0]} {leaderboard2[1][1]} A₽ | {leaderboard2[3][0]} {leaderboard2[3][1]} A₽")
            elif board == 'ip':
                embed = discord.Embed(description=f"Coming Soon", colour=0x800080)
            elif board == 'ep':
                cursor.execute(f"SELECT party, essence_points FROM server ORDER BY 2 DESC LIMIT 4")
                leaderboard = cursor.fetchall()
                embed = discord.Embed(title="Essence Point Leaderboard", description=f":first_place: Party {str.upper(leaderboard[0][0])} with {leaderboard[0][1]} E₽!\n :second_place: Party {str.upper(leaderboard[1][0])} with {leaderboard[1][1]} E₽!\n :third_place: Party {str.upper(leaderboard[2][0])} with {leaderboard[2][1]} E₽!\n :medal: Party {str.upper(leaderboard[3][0])} with {leaderboard[3][1]} E₽!", colour=0x800080, timestamp=datetime.utcnow())
            elif board == 'c':
                cursor.execute(f"SELECT member_id, user_count FROM users GROUP BY member_id ORDER BY 2 DESC LIMIT 10")
                leaderboard = cursor.fetchall()
                embed = discord.Embed(title="Counting Leaderboard", description=f":first_place: <@{leaderboard[0][0]}> with {leaderboard[0][1]} counted!\n :second_place: <@{leaderboard[1][0]}> with {leaderboard[1][1]} counted!\n :third_place: <@{leaderboard[2][0]}> with {leaderboard[2][1]} counted!\n :medal: <@{leaderboard[3][0]}> with {leaderboard[3][1]} counted!\n :medal: <@{leaderboard[4][0]}> with {leaderboard[4][1]} counted!\n :medal: <@{leaderboard[5][0]}> with {leaderboard[5][1]} counted!\n :medal: <@{leaderboard[6][0]}> with {leaderboard[6][1]} counted!\n :medal: <@{leaderboard[7][0]}> with {leaderboard[7][1]} counted!\n :medal: <@{leaderboard[8][0]}> with {leaderboard[8][1]} counted!\n :medal: <@{leaderboard[9][0]}> with {leaderboard[9][1]} counted!", colour=0x800080, timestamp=datetime.utcnow())
            else:
                embed = discord.Embed(title="Leaderboards", description=f"ap = activity points\npp = party points\nep = essence points\nc = counting", colour=0x800080, timestamp=datetime.utcnow())
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True); await self.command_logs.send(embed=embed)

async def setup(bot: commands.Bot):
    print("Commands Cog Ready")
    await bot.add_cog(Essence(bot), guilds=[discord.Object(id=725164114506285066)])