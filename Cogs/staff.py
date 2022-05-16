import discord
import sqlite3
from datetime import datetime
from discord import app_commands
from discord.ext import commands
admin = 795441220885151784
mod = 741152373921022092

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

    @app_commands.command(description="Get the current timestamp")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def timestamp(self, interaction: discord.Interaction, added_time: int):
        member = interaction.user
        timestamp = round(datetime.now().timestamp())
        timestamp = timestamp + added_time
        embed = discord.Embed(description=f"Timestamp: {timestamp}, TT: <t:{timestamp}:t>", colour=0x800080)
        embed.set_author(name=(f"{member.nick}'s Command"), icon_url=member.display_avatar)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="information")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def Information(self, interaction: discord.Interaction):
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rules")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def Rules(self, interaction: discord.Interaction):
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="punish")
    @app_commands.checks.has_permissions(ban_members=True)
    async def punish(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        member = interaction.user
        print(member)
        user_id = member.id
        channel = self.bot.get_channel(920479737405644830)
        dm_channel = await member.create_dm()
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT user_punishments FROM users WHERE user_id = ?", (user_id,))
            user_punishments = cursor.fetchone()
            if user_punishments == None:
                user_punishments = 0
            else:
                user_punishments = user_punishments[0]
        print('1')
        user_punishments = user_punishments + 1
        sql = "UPDATE users SET user_punishments = ? WHERE user_id = ?"
        print('2')
        val = (user_punishments, user_id)
        cursor.execute(sql, val)
        db.commit()
        print('3')
        embed = discord.Embed(description=f"{member} has been punished {user_punishments} times.", colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=(f"{member}'s Command"), icon_url=member.display_avatar)
        await channel.send(embed=embed)
        await interaction.message.delete
        if user_punishments == 1:
            embed = discord.Embed(description=f"Please don't break rules in Essence. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
        elif user_punishments == 2:
            embed = discord.Embed(description=f"Please stop breaking the rules in Essence. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
        elif user_punishments == 3:
            embed = discord.Embed(description=f"You are on timeout for 1 hour in Essence, please stop breaking the rules. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
            await member.timeout(3600, reason=reason)
            pass #1 hour timeout and verbal warning
        elif user_punishments == 4:
            embed = discord.Embed(description=f"You are on timeout for 8 hours in Essence, this is your last warning. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
            await member.timeout(28800, reason=reason)
            pass #8 hour timeout and verbal warning
        elif user_punishments == 5:
            embed = discord.Embed(description=f"You are on timeout for 1 day in Essence. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
            await member.timeout(86400, reason=reason)
            pass #1 day timeout
        elif user_punishments == 6:
            embed = discord.Embed(description=f"You are on timeout for 1 week in Essence. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
            await member.timeout(604800, reason=reason)
            pass #1 week timeout
        elif user_punishments == 7:
            embed = discord.Embed(description=f"You have been permanently banned from Essence. Reason: {reason}", colour=0xFF0000)
            await dm_channel.send(embed=embed)
            await member.ban(reason=reason)


    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def promote(self, interaction: discord.Interaction, arg: discord.Member = None, *, kwarg: str or None):
        member = arg
        member_id = member.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
        sql = "UPDATE users SET party_rank = ? WHERE user_id = ?"
        val = (kwarg, member_id)
        cursor.execute(sql, val)
        db.commit()
        await interaction.response.send_message(f"{member}'s party rank has been set to {kwarg}")

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, messages: int):
        await interaction.channel.purge(limit = messages + 1)
        await interaction.response.send_message(f"The messages have been deleted!")

    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def award(self, interaction: discord.Interaction, arg: discord.Member, kwarg: int):
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
            await interaction.response.send_message(f"{member} has been awarded with {kwarg} party points.")
        else:
            await interaction.response.send_message(f"{member} has lost {(kwarg * -1)} party points.")
        return

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
    
    @commands.Cog.listener() # On member leave ----------------------------------------------------------------------------------------------------------------------------------------------------
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

    @commands.Cog.listener() # Message sent --------------------------------------------------------------------------------------------------------------------------------------------------------
    async def on_message(self, message: discord.Message):
        if message.guild == None:
            return
        if message.author.id == 920471516817260564:
            return

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
                embed = discord.Embed(description=f"**{message.author} tried to hog the story**", colour=0x800080)
                await message.channel.send(embed=embed, delete_after=3)
                await message.delete()

            elif message.content.lower() == 'the end':
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                purge_amount = round(len(story.split()) / 2)
                await message.channel.purge(limit=purge_amount + 2)
                embed = discord.Embed(description=f"**THE END, sent by {message.author}**\n```{story}```\n\nIf you want to save the story, please copy and paste it now or else it will be deleted forever at the end of the next story!", colour=0x800080)
                await message.channel.send(embed=embed)
                sql = "UPDATE server SET story = ?, writer = ? WHERE party = ?"
                val = (None, None, config_line)
                cursor.execute(sql, val)
                db.commit()
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

            elif not len(message.content.split()) == 2:
                embed = discord.Embed(description=f"**{message.author} didn't say 2 words**", colour=0x800080)
                await message.channel.send(embed=embed, delete_after=3)
                await message.delete()

            else:
                if story == 'None':
                    story = message.content
                else:
                    story = story + ' ' + message.content
                sql = "UPDATE server SET story = ?, writer = ? WHERE party = ?"
                val = (story, user_id, config_line)
                cursor.execute(sql, val)
                db.commit()

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
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)
            elif int(message.content) == count + 1:
                if user_count < count + 1:
                    sql = "UPDATE users SET user_count = ? WHERE user_id = ?"
                    val = (count + 1, user_id)
                    cursor.execute(sql, val)
                sql = "UPDATE server SET count = ?, counter = ? WHERE party = ?"
                val = (count + 1, user_id, config_line)
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
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)

        if message.channel == self.bot.get_channel(735131468145360917): # commands
            if not message.author.id == 920471516817260564:
                embed = discord.Embed(description=f"**Deleted Message from {message.author} in {message.channel}**:\n{message.content}", colour=0x800080)
                await log_channel.send(embed=embed)
                await message.delete()

        if message.channel == self.bot.get_channel(940775609183924304): # no mic
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