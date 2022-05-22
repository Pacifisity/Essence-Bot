import discord
import sqlite3
import pytz
import asyncio
import sqlite3
import random
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

def voice_reward(member_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
    timestamp = round(datetime.now().timestamp())
    cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (member_id,))
    ap = cursor.fetchone(); ap = ap[0]
    if ap == None:
        ap = 0
    cursor.execute(f"SELECT voice_delay FROM users WHERE user_id = ?", (member_id,))
    voice_delay = cursor.fetchone(); voice_delay = voice_delay[0]
    if voice_delay == None:
        voice_delay = 0
    cursor.execute(f"SELECT apmulti FROM users WHERE user_id = ?", (member_id,))
    ap_multi = cursor.fetchone(); ap_multi = ap_multi[0]
    if ap_multi == None:
        ap_multi = 0
        
    if ap_multi + 86400 >= timestamp:
        voice_channel_points = round((timestamp - voice_delay) / 15) + ap
    else:
        voice_channel_points = round((timestamp - voice_delay) / 30) + ap
    sql = "UPDATE users SET activity_points = ?, voice_delay = ? WHERE user_id = ?"
    val = (voice_channel_points, timestamp, member_id)
    cursor.execute(sql, val)
    db.commit()

class Staff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.task_checker())

    async def task_checker(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            timestamp = round(datetime.now().timestamp())
            test_channel = self.bot.get_channel(920479737405644830)
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()

                # Daily party point reminder
                cursor.execute(f"SELECT user_id, daily, daily_reminder, notifications FROM users ORDER BY daily DESC")
                user_daily_information = cursor.fetchall()
                for user_daily in user_daily_information:
                    member_id = user_daily[0]
                    daily = user_daily[1]
                    reminder = user_daily[2]
                    notifications = user_daily[3]
                    if daily == None or notifications == None or notifications == 0 or reminder == None or reminder == 0:
                        pass
                    elif daily <= (timestamp - 86400):
                        await test_channel.send(f"<@{member_id}> your daily party point is ready")
                        sql = "UPDATE users SET daily_reminder = ? WHERE user_id = ?"
                        val = (0, member_id)
                        cursor.execute(sql, val)
                        db.commit()
            await asyncio.sleep(10)

    @app_commands.command(description="Get the current timestamp")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def timestamp(self, interaction: discord.Interaction, added_time: int):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        timestamp = round(datetime.now().timestamp())
        timestamp = timestamp + added_time
        embed = discord.Embed(description=f"Timestamp: {timestamp}, TT: <t:{timestamp}:t>", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral = True); await command_logs.send(embed=embed)
        
    @app_commands.command(name="information")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def Information(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        embed = discord.Embed(title="**Information**", description="Essence is a fantasy gaming discord, which promotes creating a group of friends to explore the online world", colour=0x800080)
        embed.add_field(name="**Town**", value="In the town category you can find many different lovers of fantasy games and talk or mess around.", inline=False)
        embed.add_field(name="**Parties**", value="Parties are a fundamental part of Essence and allow you to group up and compete against others in competitive and casual ways.")
        embed.add_field(name="**Events**", value="Events are held weekly for the parties and can arrange various scenarios so if you aren't able to participate in one event, chances are you'll be able to make the next one", inline=False)
        embed.add_field(name="**Game Categories**", value="Essence has started guilds and teams in many different games, if you're interested head on over to <#737812517094555698>.", inline=False)
        embed.add_field(name="**Incremental RPG**", value="Essence's developer is also working on creating games, you can check out the most recent one by doing $help in the direct messages of <@920471516817260564>", inline=False)
        #embed.add_field(name="**Activity**", value="Activity is tracked and will be rewarded, there is also leaderboards for very active players", inline=False)
        embed.add_field(name="**Timestamps**", value="Most timestamps will be converted to your local time with discord timestamps but otherwise the server is based in E.S.T. (UTC-4)", inline=False)
        #embed.add_field(name="", value="", inline=False)
        #embed.add_field(name="**Content Creators**", value="If you create content and are consistent about it (Up to judgement by admins) you may be eligible to post content in the entertainment category accessible in the <#737812517094555698> channel.", inline=False)
        embed.add_field(name="**Invite Link**", value="Want to support Essence or invite your friends? Share our invite link! https://discord.gg/Fgyd22sB3g")
        await interaction.response.send_message(embed=embed, ephemeral = True); await command_logs.send(embed=embed)

    @app_commands.command(name="rules")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def Rules(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        embed = discord.Embed(title="Rules of Essence", description="Essence Fantasy Gaming Community Discord Rules", colour=0x800080)
        embed.add_field(name="1. Basic Respect", value="Basic respect should always be given, regardless of the topic- be that opinions, beliefs or problems.", inline=False)
        embed.add_field(name="2. Privacy", value="Privacy should also be respected at a basic level, what's said in dms/private should stay in dms/private.")
        embed.add_field(name="3. Topics", value="The channel topics are there for a reason, try to stick to them as much as possible.", inline=False)
        embed.add_field(name="4. Brain Damage", value="You have to support Josh with his brain damage, it's just a necessity. :wink:", inline=False)
        embed.add_field(name="5. Voice Chat", value="Earrape, voice changers or soundboards are only allowed under the condition that it's not bothering the conversation.", inline=False)
        embed.add_field(name="6. PG-13", value="Although this hasn't been enforced much in the past, I would like to try to keep cursing and suggestive talk to a minimum.", inline=False)
        embed.add_field(name="7. Bots", value="Do not use the bots to irritate people on purpose, until Essence can completely substitute all bots- I have to ask this of you.", inline=False)
        embed.add_field(name="8. Attachments, embeds and gifs", value="Big and spammy images can effect conversation, unless the attachment is relevant to the topic- they should be kept at a minimum.", inline=False)
        embed.add_field(name="9. Links and self-advertisement", value="You're not allowed to advertise using this server as a medium unless you have explicit permission from staff or the user you're advertising to.", inline=False)
        embed.add_field(name="10. Safety", value="The internet is not a safe place, if you see something that doesn't look safe- please contact staff.")
        await interaction.response.send_message(embed=embed, ephemeral = True); await command_logs.send(embed=embed)

    @app_commands.command(name="punish")
    @app_commands.checks.has_permissions(ban_members=True)
    async def punish(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        member = member or interaction.user
        user_id = member.id
        dm_channel = await member.create_dm()
        command_logs = self.bot.get_channel(976519708096467025)
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT user_punishments FROM users WHERE user_id = ?", (user_id,))
            user_punishments = cursor.fetchone(); user_punishments = user_punishments[0]
            if user_punishments == None:
                user_punishments = 0
            user_punishments = user_punishments + 1
            sql = "UPDATE users SET user_punishments = ? WHERE user_id = ?"
            val = (user_punishments, user_id)
            cursor.execute(sql, val)
            db.commit()
            embed = discord.Embed(description=f"{member} has now been punished {user_punishments} times.", colour=0x800080, timestamp=datetime.utcnow())
            if user_punishments == 1:
                embed = discord.Embed(description=f"Please don't break rules in Essence, {member.name}.\nVerbal Warning Reason: {reason}", colour=0xFF0000)
            elif user_punishments == 2:
                embed = discord.Embed(description=f"Please stop breaking the rules in Essence, {member.name}.\nVerbal Warning Reason: {reason}", colour=0xFF0000)
            elif user_punishments == 3:
                embed = discord.Embed(description=f"You are on timeout for 1 hour in Essence, {member.name}, please stop breaking the rules. \n1 Hour Timeout Reason: {reason}", colour=0xFF0000)
                await member.timeout(3600, reason=reason)
            elif user_punishments == 4:
                embed = discord.Embed(description=f"You are on timeout for 8 hours in Essence, {member.name}. \n8 Hour Timeout Reason: {reason}", colour=0xFF0000)
                await member.timeout(28800, reason=reason)
            elif user_punishments == 5:
                embed = discord.Embed(description=f"You are on timeout for 1 day in Essence, {member.name}. \n1 Day Timeout Reason: {reason}", colour=0xFF0000)
                await member.timeout(86400, reason=reason)
            elif user_punishments == 6:
                embed = discord.Embed(description=f"You are on timeout for 1 week in Essence, {member.name}. \n1 Week Timeout Reason: {reason}", colour=0xFF0000)
                await member.timeout(604800, reason=reason)
            elif user_punishments == 7:
                embed = discord.Embed(description=f"You have been permanently banned from Essence, {member.name}. \nBan Reason: {reason}", colour=0xFF0000)
                await member.ban(reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await dm_channel.send(embed=embed)
            await command_logs.send(embed=embed)

    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def promote(self, interaction: discord.Interaction, arg: discord.Member = None, *, kwarg: str or None):
        command_logs = self.bot.get_channel(976519708096467025)
        member = arg
        member_id = member.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
        sql = "UPDATE users SET party_rank = ? WHERE user_id = ?"
        val = (kwarg, member_id)
        cursor.execute(sql, val)
        db.commit()
        embed = discord.Embed(description=f"{member}'s party rank has been set to {kwarg}"); await command_logs.send(f"{member}'s party rank has been set to {kwarg}", colour=0x800080)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def halp(self, ctx: commands.Context):
        command_logs = self.bot.get_channel(976519708096467025)
        with open(f'DB Storage\Other\help.txt') as txt:
            embed = discord.Embed(description=txt.read(), colour=0x800080)
            await ctx.send(embed=embed, ephemeral = True); await command_logs.send(embed=embed)

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, messages: int):
        command_logs = self.bot.get_channel(976519708096467025)
        await interaction.channel.purge(limit = messages)
        embed = discord.Embed(description=f"{messages} messages have been deleted in {interaction.channel}!", colour=0x800080); await command_logs.send(embed=embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Get information about the server")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def statistics(self, interaction: discord.Interaction):
        command_logs = self.bot.get_channel(976519708096467025)
        member = interaction.user
        embed = discord.Embed(description=f"**Server Statistics**", colour=0x800080)
        embed.add_field(name="Owner:", value=f"{interaction.guild.owner}", inline=False)
        embed.add_field(name="Members:", value=f"{interaction.guild.member_count}", inline=False)
        embed.add_field(name="Roles:", value=f"{len(interaction.guild.roles)}", inline=False)
        embed.add_field(name="Channels:", value=f"{len(interaction.guild.channels)}", inline=False)
        embed.add_field(name="Voice Channels:", value=f"{len(interaction.guild.voice_channels)}", inline=False)
        embed.add_field(name="Categories:", value=f"{len(interaction.guild.categories)}", inline=False)
        embed.add_field(name="Creation:", value=f"{discord.utils.format_dt(interaction.guild.created_at)}", inline=False)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral = True); await command_logs.send(embed=embed)

    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def award(self, interaction: discord.Interaction, arg: discord.Member, kwarg: int):
        command_logs = self.bot.get_channel(976519708096467025)
        member = arg
        member_id = member.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT party_points FROM users WHERE user_id = ?", (member_id,))
            pp = cursor.fetchone()
            party_points = pp[0] + kwarg
            sql = "UPDATE users SET party_points = ? WHERE user_id = ?"
            val = (party_points, member_id)
            cursor.execute(sql, val)
            db.commit()
            if kwarg >= 1:
                await interaction.response.send_message(f"{member} has been awarded with {kwarg} party points."); await command_logs.send(f"{member} has been awarded with {kwarg} party points.", ephemeral = True)
            else:
                await interaction.response.send_message(f"{member} has lost {(kwarg * -1)} party points."); await command_logs.send(f"{member} has lost {(kwarg * -1)} party points.", ephemeral = True)

    @app_commands.command(description="Party event command")
    @commands.has_permissions(manage_messages=True)
    async def event(self, interaction: discord.Interaction, arg: str or None):
        member = interaction.user
        member_id = member.id
        admin = discord.utils.get(interaction.guild.roles, id=795441220885151784)
        mod = discord.utils.get(interaction.guild.roles, id=741152373921022092)
        command_logs = self.bot.get_channel(976519708096467025)

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

        if arg == "roll":
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
            await interaction.response.send_message(embed=embed); await command_logs.send(embed=embed)

        else:
            embed = discord.Embed(description=f"There seems to be a problem with the kind of party you want to have.", colour=0x800080)
            embed.set_author(name=(f"{member.nick}'s Error"), icon_url=member.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral = True); await command_logs.send(embed=embed)
    
    @commands.Cog.listener() # Activity points for spending time in voice channels
    async def on_voice_state_update(self, member, before, after):
        member_id = member.id
        timestamp = round(datetime.now().timestamp())
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
        if not before.channel and after.channel:
            sql = "UPDATE users SET voice_delay = ? WHERE user_id = ?"
            val = (timestamp, member_id)
            cursor.execute(sql, val)
            db.commit()
        if before.channel and after.channel:
            pass
        if after.self_deaf:
            if after.afk:
                return
            else:
                voice_reward(member_id)
        if before.self_deaf and not after.self_deaf:
            if after.afk:
                return
            else:
                sql = "UPDATE users SET voice_delay = ? WHERE user_id = ?"
                val = (timestamp, member_id)
                cursor.execute(sql, val)
                db.commit()
        if after.afk:
            if not before.channel:
                pass
            if before.channel:
                voice_reward(member_id)
        if before.afk:
            sql = "UPDATE users SET voice_delay = ? WHERE user_id = ?"
            val = (timestamp, member_id)
            cursor.execute(sql, val)
            db.commit()
        if not after.channel:
            voice_reward(member_id)
        return
    
    @commands.Cog.listener() # on member join ------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(750801805490913362)
        user_id = member.id
        visitor = discord.utils.get(member.guild.roles, id=(867097611323310082))
        timestamp = round(datetime.now().timestamp())

        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
        cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        cursor.execute(f"SELECT party from users WHERE user_id = ?", (user_id,))
        party = cursor.fetchone()
        if not party == None:
            party = party[0]
            if party == "Spirit":
                spirit = discord.utils.get(member.guild.roles, id=(926660576980111370))
                await member.add_roles(spirit)
            if party == "Mana":
                mana = discord.utils.get(member.guild.roles, id=(926660721054462083))
                await member.add_roles(mana)
            if party == "Aura":
                aura = discord.utils.get(member.guild.roles, id=(926660747713474600))
                await member.add_roles(aura)
            if party == "Nature":
                nature = discord.utils.get(member.guild.roles, id=(928466489588191322))
                await member.add_roles(nature)
        if result == None:
            sql = "INSERT INTO users(user_id, activity_points, message_delay) VALUES (?, ?, ?)"
            val = (user_id, 0, timestamp)
            cursor.execute(sql, val)
            db.commit()
            print("User added to database")
        await member.add_roles(visitor)
        embed = discord.Embed(description=f"{member.mention} has joined our community :clap:", color=0xFFFFFF)
        await channel.send(embed=embed)
    
    @commands.Cog.listener() # on member leave ----------------------------------------------------------------------------------------------------------------------------------------------------
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(750801805490913362)
        embed = discord.Embed(description=f"{member.mention} has left our community :sob:")
        await channel.send(embed=embed)
        
    @commands.Cog.listener() # Message deleted ------------------------------------------------------------------------------------------------------------------------------------------------------
    async def on_message_delete(self, message: discord.Message):
        if message.guild == None:
            return
        if message.author.id == 920471516817260564:
            return
        
        log_channel = self.bot.get_channel(932351834734096494)
        
        embed = discord.Embed(description=f"**Deleted Message from {message.author} in {message.channel}**:\n{message.content}", colour=0x800080)
        await log_channel.send(embed=embed)

    @commands.Cog.listener() # message sent --------------------------------------------------------------------------------------------------------------------------------------------------------
    async def on_message(self, message: discord.Message):
        if message.guild == None:
            return
        if message.author.id == 920471516817260564:
            return
        shout_out = self.bot.get_channel(750801805490913362)
        log_channel, log_channel2 = self.bot.get_channel(932351834734096494), self.bot.get_channel(969009985512157194)
        user_id = message.author.id
        timestamp = round(datetime.now().timestamp())
        config_line = 'spirit'
        
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT count, counter FROM server WHERE party = ?", (config_line,))
            counting_information = cursor.fetchone(); count = counting_information[0]; counter = counting_information[1]
            cursor.execute(f"SELECT story, writer FROM server WHERE party = ?", (config_line,))
            story_information = cursor.fetchone(); story = str(story_information[0]); writer = story_information[1]
            cursor.execute(f"SELECT user_count FROM users WHERE user_id = ?", (user_id,))
            user_count = cursor.fetchone(); user_count = user_count[0]
            cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
        
        if message.channel == self.bot.get_channel(975885688681680986): # two word story ---------------------------------------------------------------------------------------------------------------------
            if writer == user_id:
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                embed = discord.Embed(description=f"**{message.author} tried to hog the story**", colour=0x800080)
                await message.channel.send(embed=embed, delete_after=3)
                await message.delete()
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

            elif message.content.lower() == 'the end':
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                await message.channel.purge(limit=2)
                embed = discord.Embed(description=f"**THE END, sent by {message.author}**\n```{story}```\n\nIf you want to save the story, please copy and paste it now or else it will be deleted forever at the end of the next story!", colour=0x800080)
                await message.channel.send(embed=embed)
                sql = "UPDATE server SET story = ?, writer = ? WHERE party = ?"
                val = (None, None, config_line)
                cursor.execute(sql, val)
                db.commit()
                if len(story.split()) > 249:
                    embed = discord.Embed(description=f"**The story in two word story made it to**:\n{len(story.split())} words\n\n```{story}```", colour=0x800080)
                    await shout_out.send(embed=embed)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

            elif not len(message.content.split()) == 2:
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                embed = discord.Embed(description=f"**{message.author} didn't say 2 words**", colour=0x800080)
                await message.channel.send(embed=embed, delete_after=3)
                await message.delete()
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

            else:
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                if story == 'None':
                    story = message.content
                else:
                    story = story + ' ' + message.content
                sql = "UPDATE server SET story = ?, writer = ? WHERE party = ?"
                val = (story, user_id, config_line)
                cursor.execute(sql, val)
                db.commit()
                await message.channel.purge(limit=2)
                embed = discord.Embed(description=f"Current Story:```\n{story}```\nLast author: <@{user_id}>", colour=0x800080)
                await message.channel.send(embed=embed)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

        if message.channel == self.bot.get_channel(975549476880154644): # counting ---------------------------------------------------------------------------------------------------------------------
            if user_count == None:
                user_count = 0
            if not message.content.isdigit():
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                sql = "UPDATE server SET count = ? WHERE party = ?"
                val = (0, config_line)
                cursor.execute(sql, val)
                db.commit()
                await message.channel.purge(limit=count + 10)
                embed = discord.Embed(description=f"**Non integer sent by {message.author}**:\n{message.content}", colour=0x800080)
                await message.channel.send(embed=embed)
                if count > 999:
                    embed = discord.Embed(description=f"**The count in counting made it to**:\n{count}", colour=0x800080)
                    await shout_out.send(embed=embed)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            elif counter == user_id:
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                sql = "UPDATE server SET count = ? WHERE party = ?"
                val = (0, config_line)
                cursor.execute(sql, val)
                db.commit()
                await message.channel.purge(limit=count + 10)
                embed = discord.Embed(description=f"**Double input from {message.author}**:\n{message.content}", colour=0x800080)
                await message.channel.send(embed=embed)
                if count > 999:
                    embed = discord.Embed(description=f"**The count in counting made it to**:\n{count}", colour=0x800080)
                    await shout_out.send(embed=embed)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            elif int(message.content) == count + 1:
                sql = "UPDATE server SET count = ?, counter = ? WHERE party = ?"
                val = (count + 1, user_id, config_line)
                cursor.execute(sql, val)
                sql = "UPDATE users SET user_count = ? WHERE user_id = ?"
                val = (user_count + 1, user_id)
                cursor.execute(sql, val)
                db.commit()
            else:
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                sql = "UPDATE server SET count = ? WHERE party = ?"
                val = (0, config_line)
                cursor.execute(sql, val)
                db.commit()
                await message.channel.purge(limit=count + 10)
                embed = discord.Embed(description=f"**Wrong Number from {message.author}**:\n{message.content}", colour=0x800080)
                await message.channel.send(embed=embed)
                if count > 999:
                    embed = discord.Embed(description=f"**The count in counting made it to**:\n{count}", colour=0x800080)
                    await shout_out.send(embed=embed)
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

        if message.channel == self.bot.get_channel(976345658644631623): # commands ----------------------------------------------------------------------------------------------------------------------------------------------------------------
            if not message.author.id == 920471516817260564 or not message.author.id == 547905866255433758:
                embed = discord.Embed(description=f"**Deleted Message from {message.author} in {message.channel}**:\n{message.content}", colour=0x800080)
                await log_channel.send(embed=embed)
                await message.delete()

        if message.channel == self.bot.get_channel(940775609183924304): # no mic ----------------------------------------------------------------------------------------------------------------------------------------------------------------
            if not message.author.id == 920471516817260564:
                voice_state = message.author.voice
                if voice_state == None:
                    embed = discord.Embed(description=f"**Deleted Message from {message.author} in {message.channel}**:\n{message.content}", colour=0x800080)
                    await log_channel.send(embed=embed)
                    await message.delete()
                    await message.channel.send(f"You can't talk here because you are not in a voice channel, {message.author.mention}", delete_after=5)
                    
        if result == None: # activity points ----------------------------------------------------------------------------------------------------------------------------------------------------------------
            sql = "INSERT INTO users(user_id, activity_points, message_delay) VALUES (?, ?, ?)"
            val = (user_id, 1, timestamp)
            print("User added to database")
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT message_delay FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            if timestamp <= (result[0] + 5):
                return
            else:
                cursor.execute(f"SELECT apmulti FROM users WHERE user_id = ?", (user_id,))
                apmulti = cursor.fetchone()
                if apmulti[0] == None:
                    cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (user_id,))
                    result = cursor.fetchone()
                    activity_points = result[0] + 1
                    sql = "UPDATE users SET activity_points = ?, message_delay = ? WHERE user_id = ?"
                    val = (activity_points, timestamp, user_id)
                    cursor.execute(sql, val)
                    db.commit()
                elif apmulti[0] + 86400 >= timestamp:
                    cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (user_id,))
                    result = cursor.fetchone()
                    activity_points = result[0] + 2
                    sql = "UPDATE users SET activity_points = ?, message_delay = ? WHERE user_id = ?"
                    val = (activity_points, timestamp, user_id)
                    cursor.execute(sql, val)
                    db.commit()
                else:
                    cursor.execute(f"SELECT activity_points FROM users WHERE user_id = ?", (user_id,))
                    result = cursor.fetchone()
                    activity_points = result[0] + 1
                    sql = "UPDATE users SET activity_points = ?, message_delay = ? WHERE user_id = ?"
                    val = (activity_points, timestamp, user_id)
                    cursor.execute(sql, val)
                    db.commit()

        if message.channel == log_channel or message.channel == log_channel2:
            return
        elif isinstance(message.channel, discord.channel.DMChannel):
            return
        embed = discord.Embed(description=f"**Message from {message.author} in {message.channel}**:\n{message.content}", colour=0x800080)
        await log_channel.send(embed=embed)
    
async def setup(bot: commands.Bot):
    print("Staff Cog Ready")
    await bot.add_cog(Staff(bot), guilds=[discord.Object(id=725164114506285066)])

