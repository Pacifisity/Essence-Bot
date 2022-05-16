import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime

mod = 741152373921022092

class Essence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description="Write a note you can pull up at any time")
    async def note(self, interaction: discord.Interaction, options: str, note: str):
        member = interaction.user
        note_check = note.count('@')
        if not note_check > 0:
            print(note)
        else:
            print("Pain, don't try that")


    @app_commands.command(description="Gives you the artist role and access to talk in the art channel")
    async def artist(self, interaction: discord.Interaction):
        member = interaction.user
        artist = discord.utils.get(interaction.guild.roles, id=758084699007746179)
        await member.add_roles(artist)
        embed = discord.Embed(description=f"You have been given the artist role, remember to follow the channel topics and look at pins to keep it clean.", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Gives you the supporter role and access to the entertainment category")
    async def supporter(self, interaction: discord.Interaction):
        member = interaction.user
        supporter = discord.utils.get(interaction.guild.roles, id=741720677308039278)
        await member.add_roles(supporter)
        embed = discord.Embed(description=f"You have been given the supporter role, access to entertainment channels has been given", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Changes your nickname based on the format 'Nick - Username'")
    async def nick(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        await member.edit(nick=f"{arg} - {member.name}")
        embed = discord.Embed(description=f"Your nickname has been updated, {member.mention}", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Josh's character description.")
    @app_commands.checks.has_role(mod)
    async def josh(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(description=f"https://clips.twitch.tv/SpoopyTallNightingaleHeyGuys It all started when I was a wee lad.  I was an avid evil hunter at the time, so whenever I came across anyone with an evil reputation, I hunted them. It was on one such fine evening that I found my quarry. A certain Bill Gates. After I killed him he respawned and came after me, but with backup. I did my best but alas, I could not 1v2, so I retreated into the forest, all the while taunting in chat. I thought I had earned a well-deserved respite, but only a few moments later the tree I was standing in disintegrated. They had found me. So I ran. I am unsure of what happened during this time, but a bit after my escape into the forest, one of the friends of Bill Gates sent me a message I think. I really don't know how it happened but I was somehow pulled into Discord with a man named Crystal. One thing led to another and I got roped into the guild called Acquisitive.” ~Josh", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Make a suggestion!")
    async def suggest(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        if arg == None:
            embed = discord.Embed(description=f"There seems to be a problem with your suggestion, {member}!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        else:
            channel = self.bot.get_channel(927368289821294612)
            embed = discord.Embed(description=f"{arg} suggested by <@{member.id}>", colour=0x800080)
            await channel.send(embed=embed)
            embed = discord.Embed(description=f"Your suggestion has been sent to the organizer.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Get the bot latency")
    async def ping(self, interaction: discord.Interaction):
        member = interaction.user
        embed = discord.Embed(description=f"Pong! {round(self.bot.latency * 1000)}ms", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Set the bot's status")
    async def setstatus(self, interaction: discord.Interaction, *, status: str):
        member = interaction.user
        party = 'spirit'
        if len(status) < 129:
            await self.bot.change_presence(activity=discord.Game(name=status))
            embed = discord.Embed(description="Bot status set to `Playing " + str(status) + "`", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
            sql = "UPDATE server SET status = ? WHERE party = ?"
            val = (status, party)
            cursor.execute(sql, val)
            db.commit()
        else:
            embed = discord.Embed(description=f"Too many characters, the bot's status can't support more than 128 characters.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Look at the different leaderboards")
    async def leaderboard(self, interaction: discord.Interaction, board: str):
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
        if board == 'pp':
            cursor.execute(f"SELECT user_id, party_points, party FROM users GROUP BY user_id ORDER BY 2 DESC LIMIT 10")
            lb = cursor.fetchall()
            cursor.execute(f"SELECT party, SUM(party_points) FROM users GROUP BY party")
            lb2 = cursor.fetchall()
            embed = discord.Embed(title="Party Point Leaderboard", description=f":first_place: <@{lb[0][0]}> {lb[0][2]} member with {lb[0][1]} ₽₽!\n :second_place: <@{lb[1][0]}> {lb[1][2]} member with {lb[1][1]} ₽₽!\n :third_place: <@{lb[2][0]}> {lb[2][2]} member with {lb[2][1]} ₽₽!\n :medal: <@{lb[3][0]}> {lb[3][2]} member with {lb[3][1]} ₽₽!\n :medal: <@{lb[4][0]}> {lb[4][2]} member with {lb[4][1]} ₽₽!\n :medal: <@{lb[5][0]}> {lb[5][2]} member with {lb[5][1]} ₽₽!\n :medal: <@{lb[6][0]}> {lb[6][2]} member with {lb[6][1]} ₽₽!\n :medal: <@{lb[7][0]}> {lb[7][2]} member with {lb[7][1]} ₽₽!\n :medal: <@{lb[8][0]}> {lb[8][2]} member with {lb[8][1]} ₽₽!\n :medal: <@{lb[9][0]}> {lb[9][2]} member with {lb[9][1]} ₽₽!", colour=0x800080, timestamp=datetime.utcnow())
            embed.add_field(name="Cumulative party points", value=f"{lb2[4][0]} {lb2[4][1]} ₽₽ | {lb2[2][0]} {lb2[2][1]} ₽₽ | {lb2[1][0]} {lb2[1][1]} ₽₽ | {lb2[3][0]} {lb2[3][1]} ₽₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        if board == 'ap':
            cursor.execute(f"SELECT user_id, activity_points, party FROM users GROUP BY user_id ORDER BY 2 DESC LIMIT 10")
            lb = cursor.fetchall()
            cursor.execute(f"SELECT party, SUM(activity_points) FROM users GROUP BY party")
            lb2 = cursor.fetchall()
            embed = discord.Embed(title="Activity Point Leaderboard", description=f":first_place: <@{lb[0][0]}> {lb[0][2]} member with {lb[0][1]} A₽!\n :second_place: <@{lb[1][0]}> {lb[1][2]} member with {lb[1][1]} A₽!\n :third_place: <@{lb[2][0]}> {lb[2][2]} member with {lb[2][1]} A₽!\n :medal: <@{lb[3][0]}> {lb[3][2]} member with {lb[3][1]} A₽!\n :medal: <@{lb[4][0]}> {lb[4][2]} member with {lb[4][1]} A₽!\n :medal: <@{lb[5][0]}> {lb[5][2]} member with {lb[5][1]} A₽!\n :medal: <@{lb[6][0]}> {lb[6][2]} member with {lb[6][1]} A₽!\n :medal: <@{lb[7][0]}> {lb[7][2]} member with {lb[7][1]} A₽!\n :medal: <@{lb[8][0]}> {lb[8][2]} member with {lb[8][1]} A₽!\n :medal: <@{lb[9][0]}> {lb[9][2]} member with {lb[9][1]} A₽!", colour=0x800080, timestamp=datetime.utcnow())
            embed.add_field(name="Cumulative party points", value=f"{lb2[4][0]} {lb2[4][1]} A₽ | {lb2[2][0]} {lb2[2][1]} A₽ | {lb2[1][0]} {lb2[1][1]} A₽ | {lb2[3][0]} {lb2[3][1]} A₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        if board == 'ip':
            embed = discord.Embed(description=f"Coming Soon", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        if board == 'ep':
            cursor.execute(f"SELECT party, essence_points FROM server ORDER BY 2 DESC LIMIT 4")
            lb = cursor.fetchall()
            embed = discord.Embed(title="Essence Point Leaderboard", description=f":first_place: Party {str.upper(lb[0][0])} with {lb[0][1]} E₽!\n :second_place: Party {str.upper(lb[1][0])} with {lb[1][1]} E₽!\n :third_place: Party {str.upper(lb[2][0])} with {lb[2][1]} E₽!\n :medal: Party {str.upper(lb[3][0])} with {lb[3][1]} E₽!", colour=0x800080, timestamp=datetime.utcnow())
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        if board == 'c':
            cursor.execute(f"SELECT user_id, user_count FROM users GROUP BY user_id ORDER BY 2 DESC LIMIT 10")
            lb = cursor.fetchall()
            embed = discord.Embed(title="Counting Leaderboard", description=f":first_place: <@{lb[0][0]}> with {lb[0][1]} high score!\n :second_place: <@{lb[1][0]}> with {lb[1][1]} high score!\n :third_place: <@{lb[2][0]}> with {lb[2][1]} high score!\n :medal: <@{lb[3][0]}> with {lb[3][1]} high score!\n :medal: <@{lb[4][0]}> with {lb[4][1]} high score!\n :medal: <@{lb[5][0]}> with {lb[5][1]} high score!\n :medal: <@{lb[6][0]}> with {lb[6][1]} high score!\n :medal: <@{lb[7][0]}> with {lb[7][1]} high score!\n :medal: <@{lb[8][0]}> with {lb[8][1]} high score!\n :medal: <@{lb[9][0]}> with {lb[9][1]} high score!", colour=0x800080, timestamp=datetime.utcnow())
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    print("Commands Cog Ready")
    await bot.add_cog(Essence(bot), guilds=[discord.Object(id=725164114506285066)])