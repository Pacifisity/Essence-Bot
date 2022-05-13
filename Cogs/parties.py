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
    async def info(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        arg = str.lower(arg)

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
            await interaction.response.send_message(embed=embed)

        elif arg == "mana":
            embed = discord.Embed(title="Party Mana", description="Party led by <@261900816841965570>, those who join party mana want to take control of Essence energy. ($party mana)",  colour=0xd6680e)
            embed.add_field(name="Party Mana Points:", value=f"{party_total[2][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "aura":
            embed = discord.Embed(title="Party Aura", description="Party led by <@508504220354347018>, those who join party aura want to use Essence energy as an external power. ($party aura)",  colour=0xca0a0a)
            embed.add_field(name="Party Aura Points:", value=f"{party_total[1][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "nature":
            embed = discord.Embed(title="Party Nature", description="Those who join the nature party want essence to be left in it's base form, unmanipulated and naturally flowing. ($party nature)",  colour=0x00ff00)
            embed.add_field(name="Party Nature Points:", value=f"{party_total[3][1]} P₽")
            embed.add_field(name="Party Essence Points:", value=f"{essence_points[0]} E₽")
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        
        else:
            embed = discord.Embed(title="Parties", description=f"Parties are teams, party **spirit**, party **mana**, party **aura** and party **nature**. Each party is competing against the other party for party points (₽₽) and essence points (TBD). These points will be used in leaderboards and as a currency for a shop in the coming future. Events can be from 3v3v3v3 battle royales to a pet picture competition :wink:!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Join a party!")
    async def join(self, interaction: discord.Interaction, arg: str or None):
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
                await interaction.response.send_message(embed=embed)

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
                await interaction.response.send_message(embed=embed)

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
                await interaction.response.send_message(embed=embed)

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
                await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(title="Parties", description=f"Which party would you like to join?\n\nParties are teams, party **spirit**, party **mana**, party **aura** and party **nature**. Each party is competing against the other party for party points (₽₽) and essence points (TBD). These points will be used in leaderboards and as a currency for a shop in the coming future. Events can be from 3v3v3v3 battle royales to a pet picture competition :wink:!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Leave a party")
    async def leave(self, interaction: discord.Interaction, arg: str or None):
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
                    await interaction.response.send_message(embed=embed)
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
                    await interaction.response.send_message(embed=embed)
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
                    await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Are you sure you want to leave your party?", description="If you are sure you want to leave your party do /party leave confirm\n\nIf you leave your party, you will lose you party rank and any extra party points. Spend all party points above 10 before you leave your party.",  colour=0x00ff00)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Collect your daily party point")
    async def daily(self, interaction: discord.Interaction):
        impurity = discord.utils.get(interaction.guild.roles, id=934956487107813426) 
        timestamp = round(datetime.now().timestamp())
        member = interaction.user
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member.id,))
            party_points = cursor.fetchone(); party_points = party_points[0]
            cursor.execute(f"SELECT party FROM users WHERE user_id = ?", (member.id,))
            party = cursor.fetchone(); party = party[0]
            cursor.execute(f"SELECT brain_pills FROM users WHERE user_id = ?", (member.id,))
            brain_pills = cursor.fetchone(); brain_pills = brain_pills[0]
            if brain_pills == None:
                brain_pills = 0
            cursor.execute(f"SELECT daily FROM users WHERE user_id = ?", (member.id,))
            daily_cooldown = cursor.fetchone(); daily_cooldown = daily_cooldown[0]
            if daily_cooldown == None:
                daily_cooldown = 0
            
        if party == None:
            embed = discord.Embed(description=f"You have to join a party first!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
            return

        if daily_cooldown >= (timestamp - 86400):
            embed = discord.Embed(description=f"You can claim your daily <t:{daily_cooldown + 86400}:R> (<t:{daily_cooldown + 86400}:t>)", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
            return

        if not daily_cooldown >= (timestamp - 86400):
            embed = discord.Embed(description=f"Daily point claimed!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            pill = random.randint(1,10)
            party_points += 1
            sql = "UPDATE users SET party_points = ?, daily = ? WHERE user_id = ?"
            val = (party_points, timestamp, member.id)
            cursor.execute(sql, val)
            db.commit()
            if pill == 1:
                embed.add_field(name='-', value="You've gained a brain bean!")
                sql = "UPDATE users SET brain_pills = ? WHERE user_id = ?"
                val = (brain_pills + 1, member.id)
                cursor.execute(sql, val)
                db.commit()
            
        if impurity in member.roles:
            embed.add_field(value="You've been cleansed from your impurity")
            await member.remove_roles(impurity)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Party event command")
    async def event(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        member_id = member.id
        participant = discord.utils.get(interaction.guild.roles, id=959574821228933183)
        admin = discord.utils.get(interaction.guild.roles, id=795441220885151784)
        mod = discord.utils.get(interaction.guild.roles, id=741152373921022092)
        
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member_id,))
            party_points = cursor.fetchone()
            party_points = party_points[0]
            cursor.execute(f"SELECT pp_storage FROM users WHERE user_id = ?", (member_id,))
            pp = cursor.fetchone()
            pp = pp[0]
            cursor.execute(f"SELECT party FROM users WHERE user_id = ?", (member_id,))
            party = cursor.fetchone()
            party = party[0]
            cursor.execute(f"SELECT event_participants FROM server WHERE party = ?", ("event",))
            event_participants = cursor.fetchone()
            event_participants = event_participants[0]
            cursor.execute(f"SELECT event_admins FROM server WHERE party = ?", ("event",))
            event_admins = cursor.fetchone()
            event_admins = event_admins[0]

        if arg == "ping":
            EventPings = discord.utils.get(interaction.guild.roles, id=927757185889488956) 
            await member.add_roles(EventPings)
            embed = discord.Embed(description=f"You will be notified for all future events!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        if arg == "leave":
            if participant in member.roles:
                await member.remove_roles(participant)
                if member.id == event_admins:
                    sql = "UPDATE server SET event_admins = ? WHERE party = ?"
                    val = (None, "event")
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(description=f"You are no longer supervising this event!", colour=0x800080)
                else:
                    sql = "UPDATE server SET event_participants = ? WHERE party = ?"
                    val = (event_participants - 1, "event")
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(description=f"You are no longer participating in this event!", colour=0x800080)
            else:
                embed = discord.Embed(description=f"You're not even a participant! Silly!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "roll":
            if admin in member.roles or mod in member.roles:
                event = random.randint(1,10)
                if event == 1:
                    embed = discord.Embed(description=f"__**New Event!**__\n**The supervisor will provide the hyperlink**\nParticipants will work with the supervisor to create a new fun event to add to our list of events to enjoy in the future!", colour=0x800080)
                elif event == 2:
                    embed = discord.Embed(description=f"__**Music related event**__\n**You will split up into your party specific voice channels**\nEvery party will go into party specific voice channels and create a single song under the category the supervisor gives, best fit for that category will be chosen by the supervisor. Party whose song is chosen gains the essence point (cards against humanity style)", colour=0x800080)
                elif event == 3:
                    embed = discord.Embed(description=f"__**Randomized Roblox War**__\n**The supervisor will provide the hyperlink**\nThe supervisor will choose random roblox games and rules and then the parties will do their best to compete. You get 1 point per game you win and whichever party gains the most points gets the essence point (supervisors have lots of freedom with this one)", colour=0x800080)
                elif event == 4:
                    embed = discord.Embed(description=f"__**Random Shooter Game**__\n**The supervisor will provide the hyperlink**\nThe supervisor will choose a random Shooter game and will create a private lobby for each team to compete against eachother, under the circumstance that there are not enough spots in a squad/team then pp rewards will be only given to the participants (participants will vote for who participates) and ep goes to the team with the most wins!", colour=0x800080)
                elif event == 5:
                    embed = discord.Embed(description=f"__**Participation/Chill**__\n**<#939713383433924648> or your party specific voice channels!**\nIf every party has 2 or more participants then they will split into party voice channels, otherwise <#939713383433924648> is fine. Most participants in the party wins the essence point. (You must spend atleast for 30 minutes in vc to count as participated)", colour=0x800080)
                elif event == 6:
                    embed = discord.Embed(description=f"__**Scavenger**__\n**Supervisor will send the first hyperlink**\nThe supervisor will create a hunt of some sorts across the internet, the team with the most completions of the hunt will win the essence point (If nobody gets it within the 3 hours the event lasts then everyone should make fun of the supervisor)", colour=0x800080)
                elif event == 7:
                    embed = discord.Embed(description=f"__**Among us**__\n**You can find it on steam, or on mobile**\nThis one doesn't leave much to the imagination, you will win 1 party point per imposter win. 1 imposter for 5 people and below, 2 for anything above that. Most party points gained gets the essence point (Supervisor only needs to keep track and host the game)", colour=0x800080)
                elif event == 8:
                    embed = discord.Embed(description=f"__**Gartic Telephone**__\n**Website**: https://garticphone.com/\nThis event is either a participation based event where everyone who participates for the minimum time gets points, or a best players wins event where the people who perform best get the most PP.\nGartic Telephone is a game where everyone types in their own word or phrase. Then that word or phrase gets passed on to someone else. That someone draws an image representing the word or phrase. Then that image gets passed on to the next player. This player attempts to replicate the image they see in front of them to keep the meaning of the original word or phrase. It then gets passed on to be replicated again. This continues until the very last person, where they will have to guess what the original word or phrase is based on the most recent replication. The game is based on the premise of visually trying to keep the meaning of a word or phrase and then seeing well (or not well) that word or phrases's meaning was kept. There are also multiple different game modes that are variations of the core concept.", colour=0x800080)
                elif event == 9:
                    embed = discord.Embed(description=f"__**Critical Strike**__\n**Website**: https://www.roblox.com/games/111311599\nThis event is decided by performance in a game. Individuals will compete and whoever performs the best will gain the most points.\n\nA private server will be made in the game in the link above", colour=0x800080)
                elif event == 10:
                    embed = discord.Embed(description=f"__**Rock paper scissors**__\n**Website**: https://www.rpsgame.org/\nSimple and fun, supervisor will set the rules and then you guys can go at eachother's throats! (ep will be distributed by the supervisor)", colour=0x800080)
            else:
                embed = discord.Embed(description=f"You don't have permission to use this command.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "start":
            embed = discord.Embed(description=f"The event has begun!", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "reset":
            if admin in member.roles or mod in member.roles:
                embed = discord.Embed(description=f"Please make sure that all participants after being rewarded are removed from the participants role", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
                #check if any members have the participant role
                sql = "UPDATE server SET event_participants = ?, event_admins = ? WHERE party = ?"
                val = (0, 0, "event")
                cursor.execute(sql, val)
                db.commit()
            else:
                embed = discord.Embed(description=f"You do not have permission to use this command.", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)

        elif arg == "supervise":
            if participant in member.roles:
                embed = discord.Embed(description=f"You have signed up for this week's event already!\n**{event_participants}/5** Participants\n**Supervisor: <@{event_admins}>**\n\nIf you want to supervise but have already made yourself a participant do '$p event leave'\nAll events are held on a saturday at <t:86400:t> and last up to 3 hours, the event is randomized between a list of suggestions given by the $suggest command", colour=0x800080)
            else:
                    sql = "UPDATE server SET event_admins = ? WHERE party = ?"
                    val = (member.id, "event")
                    cursor.execute(sql, val)
                    db.commit()
                    await member.add_roles(participant)
                    embed = discord.Embed(description=f"You are now supervising this event.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)

        elif arg == "join":
            #if you sign up and not enough people sign up, you will get 1 party point just for trying. If you miss an event after signing up you will get a strike- if you get 3 strikes you are out. To remove a strike you need to attend an event)
            if participant in member.roles:
                embed = discord.Embed(description=f"You have signed up for this week's event already!\n**{event_participants}/5** Participants\n**Supervisor: <@{event_admins}>**\n\nIf you can't participate in this event anymore please do '$p event leave'\nAll events are held on a saturday at <t:86400:t> and last up to 3 hours, the event is randomized between a list of suggestions given by the $suggest command", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
            else:
                sql = "UPDATE server SET event_participants = ? WHERE party = ?"
                val = (event_participants + 1, "event")
                cursor.execute(sql, val)
                db.commit()
                await member.add_roles(participant)
                embed = discord.Embed(description=f"**You have signed up for an event!**\n\nAll events are held on a saturday at <t:86400:t> and last up to 3 hours, the event is randomized between a list of suggestions given by the $suggest command", colour=0x800080)
                embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
                await interaction.response.send_message(embed=embed)
                if event_participants == 5:
                    pass#send a message in #party events that there are enough people for this weekend's party

        else:
            embed = discord.Embed(description=f"There seems to be a problem with the kind of party you want to have.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Error"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
    

async def setup(bot: commands.Bot):
    print("Party Cog Ready")
    await bot.add_cog(Party(bot), guilds=[discord.Object(id=725164114506285066)])