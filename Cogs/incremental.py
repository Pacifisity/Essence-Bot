import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import random

# Checks for a character --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def character_check(user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
        character_name = cursor.fetchone()
        character_name = character_name[0]
    if not character_name == None:
        return True
    else:
        return False

# Formats numbers --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def number_format(number):
    number = "{:,}".format(number)
    return number

# Suppresses the character's lost hp --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def hp_suppresion(hp_lost, user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT character_level, character_world_level ROM incremental WHERE user_id = ?', (user_id,))
        character_information = cursor.fetchone()
        character_level = character_information[0]
        character_world_level = character_information[1]

    # hp lost level suppresion
    max_world_level = 10 * character_world_level
    if character_level > max_world_level:
        hp_lost = (hp_lost / (1 + ((character_level - max_world_level) / 10)))
        if character_level > max_world_level + 10:
            hp_lost = hp_lost / 3 * (1 + ((character_level - max_world_level) / 10))
    
    # hp lost randomization
    hp_randomizer = random.randint(1,3)
    hp_lost = hp_lost * (0.8 + hp_randomizer / 10)

    return int(hp_lost)

# Suppresses the character's gained xp --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def xp_suppresion(xp_gained, user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT character_level FROM incremental WHERE user_id = ?', (user_id,))
        character_level = cursor.fetchone()
        character_level = character_level[0]
        cursor.execute(f'SELECT character_world_level FROM incremental WHERE user_id = ?', (user_id,))
        character_world_level = cursor.fetchone()
        character_world_level = character_world_level[0]

    # xp gain level suppresion
    max_world_level = 10 * character_world_level
    if character_level > max_world_level:
        xp_gained = xp_gained / (1 + ((character_level - max_world_level) / 10))
        if character_level > max_world_level + 10:
            xp_gained = xp_gained / 3 * (1 + ((character_level - max_world_level) / 10))
    
    # xp gain randomization
    xp_randomizer = random.randint(1,3)
    xp_gained = xp_gained * (0.8 + xp_randomizer / 10)

    return int(xp_gained)

# Updates the character's information ------------------------------------------------------------------------------------------------------------------------------------------------------------
def character_update(hp_lost, xp_gained, energy_stones_gained, user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        # character stats
        cursor = db.cursor()
        cursor.execute(f'SELECT stat_explorations FROM incremental WHERE user_id = ?', (user_id,))
        stat_explorations = cursor.fetchone(); stat_explorations = stat_explorations[0]
        cursor.execute(f'SELECT stat_damage_taken FROM incremental WHERE user_id = ?', (user_id,))
        stat_damage_taken = cursor.fetchone(); stat_damage_taken = stat_damage_taken[0]
        cursor.execute(f'SELECT stat_xp_gained FROM incremental WHERE user_id = ?', (user_id,))
        stat_xp_gained = cursor.fetchone(); stat_xp_gained = stat_xp_gained[0]
        cursor.execute(f'SELECT stat_energy_stones_gained FROM incremental WHERE user_id = ?', (user_id,))
        stat_energy_stones_gained = cursor.fetchone(); stat_energy_stones_gained = stat_energy_stones_gained[0]

        # character information
        cursor.execute(f'SELECT character_xp FROM incremental WHERE user_id = ?', (user_id,))
        character_xp = cursor.fetchone(); character_xp = character_xp[0]
        cursor.execute(f'SELECT character_energy_stones FROM incremental WHERE user_id = ?', (user_id,))
        character_energy_stones = cursor.fetchone(); character_energy_stones = character_energy_stones[0]
        cursor.execute(f'SELECT character_hp FROM incremental WHERE user_id = ?', (user_id,))
        character_hp = cursor.fetchone(); character_hp = character_hp[0]

        # update's character information
        sql = "UPDATE incremental SET character_xp = ?, character_hp = ?, character_energy_stones = ? WHERE user_id = ?"
        val = ((character_xp + xp_gained), (character_hp - hp_lost), (character_energy_stones + energy_stones_gained), user_id)
        cursor.execute(sql, val)
        db.commit()

        # saves all tracked stats
        sql = "UPDATE incremental SET stat_explorations = ?, stat_xp_gained = ?, stat_damage_taken = ?, stat_energy_stones_gained = ? WHERE user_id = ?"
        val = ((stat_explorations + 1), (stat_xp_gained + xp_gained), (stat_damage_taken + hp_lost), (stat_energy_stones_gained + energy_stones_gained), user_id)
        cursor.execute(sql, val)
        db.commit()

# Checks if the character's hp has fallen below 0 and returns their death if so ----------------------------------------------------------------------------------------------------------------
def death_check(hp_lost, user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
        character_name = cursor.fetchone()
        character_name = character_name[0]
        cursor.execute(f'SELECT character_hp FROM incremental WHERE user_id = ?', (user_id,))
        character_hp = cursor.fetchone()
        character_hp = character_hp[0]
        cursor.execute(f'SELECT character_xp FROM incremental WHERE user_id = ?', (user_id,))
        character_xp = cursor.fetchone()
        character_xp = character_xp[0]
        cursor.execute(f'SELECT character_xp_required FROM incremental WHERE user_id = ?', (user_id,))
        character_xp_required = cursor.fetchone()
        character_xp_required = character_xp_required[0]

    if character_hp <= 0:
        if round(character_xp - character_xp_required * 0.2) <= 0:
            experience_after_death = 0

        else:
            experience_after_death = round(character_xp - character_xp_required * 0.2)

        character_hp = character_hp + hp_lost

        sql = "UPDATE incremental SET character_xp = ?, character_hp = ? WHERE user_id = ?"
        val = (experience_after_death, character_hp, user_id)
        cursor.execute(sql, val)
        db.commit()
        dead = True
    else:
        dead = False
    return dead

def world_lock(unlock_scenario, stat_world_keys, user_id):
    with sqlite3.connect('DB Storage/essence.db') as db:
        cursor = db.cursor()
    if unlock_scenario == 1:
        if stat_world_keys == 0:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE user_id = ?"
            val = (1, user_id)
    elif unlock_scenario == 2:
        if stat_world_keys == 1:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE user_id = ?"
            val = (2, user_id)
    elif unlock_scenario == 3:
        if stat_world_keys == 2:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE user_id = ?"
            val = (3, user_id)
    else:
        sql = "UPDATE incremental SET stat_world_keys = ? WHERE user_id = ?"
        val = (stat_world_keys, user_id)
    cursor.execute(sql, val)
    db.commit()

class Incremental(commands.Cog): #characterMaxHp
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return isinstance(ctx.channel, discord.channel.DMChannel)
        

    @commands.command(name="patch")
    async def patch(self, ctx: commands.Context, arg: str = None):
        channel = self.bot.get_channel(969009985512157194)
        if arg == None:
            arg = "2"
        with open(f'DB Storage\patchNotes\patch{arg}.txt') as n:
            embed = discord.Embed(description=n.read(), colour=0x800080)
            await ctx.send(embed=embed); await channel.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def simulate(self, ctx: commands.Context, arg: str, kwarg: int):
        user_id = ctx.author.id
        character_level = random.randint(1,30)
        channel = self.bot.get_channel(969009985512157194)
        if arg == "levels":
            output_number = 100
            counter = 0
            while True:
                output_number = round(output_number * 1.35)
                counter = counter + 1
                embed = discord.Embed(description=f"{output_number} xp - {counter + 1} level", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)
                if counter == kwarg:
                    return
        elif arg == "xp":
            xp_gained = kwarg
            xp_gained = xp_suppresion(xp_gained, user_id)
            embed = discord.Embed(description=f"LEVEL: {character_level} XP GAINED: {xp_gained}", colour=0x800080)
            await ctx.send(embed=embed); await channel.send(embed=embed)
        elif arg == "hp":
            hp_lost = kwarg
            hp_lost = xp_suppresion(hp_lost, user_id)
            embed = discord.Embed(description=f"LEVEL: {character_level} HP LOST: {hp_lost}", colour=0x800080)
            await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.command()
    async def register(self, ctx: commands.Context, *, arg: str = None):
        channel = self.bot.get_channel(969009985512157194)
        user_id = ctx.author.id
        timestamp = round(datetime.now().timestamp())
        if arg == None:
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
                cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
                character_name = cursor.fetchone()
            if not character_name == None:
                embed = discord.Embed(description=f"You've already started your journey, {character_name[0]}", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)
            else:
                embed = discord.Embed(description=f"To begin your journey, please register your character's name '$register (character name)'\n\nWelcome to the game of Essence, story based incremental rpg. In Essence you take control of a character born from Energy, plopped down in the middle of nowhere and with a multitude of scenarios to '$explore'.", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)
        else:
            with sqlite3.connect('DB Storage/essence.db') as db:
                cursor = db.cursor()
                cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
                character_name = cursor.fetchone()
            if character_name == None:
                sql = "INSERT INTO incremental(user_id, character_name, character_level, character_energy_stones, character_world_level, character_xp, character_xp_required, character_hp, stat_birthday, stat_explorations, stat_damage_taken, stat_xp_gained, stat_energy_stones_gained, stat_world_boss_damage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val = (user_id, arg, 1, 0, 1, 0, 100, 100, timestamp, 0, 0, 0, 0, 0)
                cursor.execute(sql, val)
                db.commit()
                embed = discord.Embed(description=f"Welcome to the game of Essence, your character {arg} has been created.", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)
            else:
                embed = discord.Embed(description=f"You've already started your journey, {character_name[0]}", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.command()
    async def character(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        channel = self.bot.get_channel(969009985512157194)
        user_id = ctx.author.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name, character_level, character_xp, character_xp_required, character_energy_stones, character_hp FROM incremental WHERE user_id = ?', (user_id,))
            character_information = cursor.fetchone()
            character_name = character_information[0]
            character_level = character_information[1]
            character_xp = character_information[2]
            character_xp_required = character_information[3]
            character_energy_stones = character_information[4]
            character_hp = character_information[5]
        if character_level <= 9:
            state_of_being = "Mortal"
        if character_level >= 10 and character_level <= 59:
            state_of_being = "Warrior"
        if character_level >= 60 and character_level <= 99:
            state_of_being = "Immortal"
        if character_level >= 100:
            state_of_being = "God"
        character_xp = number_format(character_xp)
        character_xp_required = number_format(character_xp_required)
        character_energy_stones = number_format(character_energy_stones)
        
        embed = discord.Embed(description="", colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=character_name, icon_url=ctx.author.display_avatar)
        embed.add_field(name="Level", value=f"{state_of_being} {character_level}", inline=True)
        embed.add_field(name="Experience", value=f"{character_xp} of {character_xp_required}", inline=True)
        embed.add_field(name="Health", value=f"{character_hp}%", inline=True)
        embed.add_field(name="energy stones", value=f"{character_energy_stones}", inline=True)
        await ctx.send(embed=embed); await channel.send(embed=embed)
    
    @commands.command()
    async def advance(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        channel = self.bot.get_channel(969009985512157194)
        user_id = ctx.author.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name, character_level, character_xp, character_xp_required, character_hp FROM incremental WHERE user_id = ?', (user_id,))
            character_information = cursor.fetchone()
            character_name = character_information[0]
            character_level = character_information[1]
            character_xp = character_information[2]
            character_xp_required = character_information[3]
            character_hp = character_information[4]
            if character_level <= 9:
                state_of_being = "Mortal"
            elif character_level <= 59 and character_level >= 10:
                state_of_being = "Warrior"
            elif character_level <= 99 and character_level >= 60:
                state_of_being = "Immortal"
            elif character_level >= 100:
                state_of_being = "God"
        if character_xp >= character_xp_required:
            embed = discord.Embed(description=f"{character_name} has advanced to {state_of_being} {character_level + 1}!", colour=0x800080)
            sql = "UPDATE incremental SET character_level = ?, character_xp = ?, character_xp_required = ? WHERE user_id = ?"
            val = (character_level + 1, 0, round(character_xp_required*1.35), user_id)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send(embed=embed); await channel.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{character_name} wasn't ready to advance and caused a backlash on their mind while trying.\n-10hp", colour=0x800080)
            sql = "UPDATE incremental SET character_hp = ? WHERE user_id = ?"
            val = (character_hp - 10, user_id)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send(embed=embed); await channel.send(embed=embed)

        dead = death_check(10, user_id)
        if dead:
            embed = discord.Embed(description=f"{character_name} died while trying to advance, they feel weaker but they don't remember dying", colour=0x800080)
            await ctx.send(embed=embed); await channel.send(embed=embed)
    
    @commands.command()
    async def world(self, ctx: commands.Context, arg: int):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        user_id = ctx.author.id
        channel = self.bot.get_channel(969009985512157194)
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name, character_world_level, stat_world_keys FROM incremental WHERE user_id = ?', (user_id,))
            character_information = cursor.fetchone()
            character_name = character_information[0]
            character_world_level = character_information[1]
            stat_world_keys = character_information[2]
            if character_world_level == arg:
                embed = discord.Embed(description=f"{character_name} decided they want to go somewhere today, but they're not sure where.", colour=0x800080)
                await ctx.send(embed=embed); await channel.send(embed=embed)
                return
            if character_world_level == 1:
                if stat_world_keys >= 3:
                    embed = discord.Embed(description=f"{character_name} steps close to the portal, they feel a pull. As they walk closer to the portal a faint pressure can be felt. The pressure is no sweat for {character_name} and they walk into the portal.", colour=0x800080)
                    sql = "UPDATE incremental SET character_world_level = ? WHERE user_id = ?"
                    val = (2, user_id)
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send(embed=embed); await channel.send(embed=embed)
            if character_world_level == 2:
                embed = discord.Embed(description=f"{character_name} travels back to the point where they first entered this world, and steps back through the portal.", colour=0x800080)
                sql = "UPDATE incremental SET character_world_level = ? WHERE user_id = ?"
                val = (1, user_id)
                cursor.execute(sql, val)
                db.commit()
                await ctx.send(embed=embed); await channel.send(embed=embed)

            

    @commands.command()
    async def recover(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        channel = self.bot.get_channel(969009985512157194)
        timestamp = round(datetime.now().timestamp())
        user_id = ctx.author.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT cooldown_rest FROM incremental WHERE user_id = ?', (user_id,))
            cooldown_rest = cursor.fetchone()
            cursor.execute(f'SELECT character_hp FROM incremental WHERE user_id = ?', (user_id,))
            character_hp = cursor.fetchone()
            cooldown_rest, character_hp = cooldown_rest[0], character_hp[0]
        if cooldown_rest == None or cooldown_rest <= timestamp - 3600:
            embed = discord.Embed(description=f"You have fully recovered!", colour=0x800080)
            sql = "UPDATE incremental SET character_hp = ?, cooldown_rest = ? WHERE user_id = ?"
            val = (100, timestamp, user_id)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send(embed=embed); await channel.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Too much recovery at once could affect the healing process. You can recover again <t:{cooldown_rest + 3600}:R>", colour=0x800080)
            await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.cooldown(rate=1, per=3)
    @commands.command()
    async def explore(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        channel = self.bot.get_channel(969009985512157194)
        user_id = ctx.author.id
        exploration_number = random.randint(1,25)
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
            character_name = cursor.fetchone(); character_name = character_name[0]
            cursor.execute(f'SELECT character_energy_stones FROM incremental WHERE user_id = ?', (user_id,))
            character_energy_stones = cursor.fetchone(); character_energy_stones = character_energy_stones[0]
            cursor.execute(f'SELECT character_level FROM incremental WHERE user_id = ?', (user_id,))
            character_level = cursor.fetchone(); character_level = character_level[0]
            cursor.execute(f'SELECT character_xp FROM incremental WHERE user_id = ?', (user_id,))
            character_xp = cursor.fetchone(); character_xp = character_xp[0]
            cursor.execute(f'SELECT character_xp_required FROM incremental WHERE user_id = ?', (user_id,))
            character_xp_required = cursor.fetchone(); character_xp_required = character_xp_required[0]
            cursor.execute(f'SELECT character_hp FROM incremental WHERE user_id = ?', (user_id,))
            character_hp = cursor.fetchone(); character_hp = character_hp[0]
            cursor.execute(f'SELECT character_world_level FROM incremental WHERE user_id = ?', (user_id,))
            character_world_level = cursor.fetchone(); character_world_level = character_world_level[0]
            cursor.execute(f'SELECT stat_world_keys FROM incremental WHERE user_id = ?', (user_id,))
            stat_world_keys = cursor.fetchone(); stat_world_keys = stat_world_keys[0]

            if stat_world_keys == None:
                stat_world_keys = 0
            hp_lost = 0; xp_gained = 0; energy_stones_gained = 0

        embed = discord.Embed(description=f"**{character_name} went on an adventure to explore the world of Essence**", colour=0x800080)
        if character_world_level == 1:

            if exploration_number == 1:
                embed.add_field(name="-", value=f"{character_name} fell down a cliff", inline=False)
                cliff_scenario = random.randint(1,10)
                if cliff_scenario <= 7:
                    hp_lost = hp_suppresion(5, user_id)
                    embed.add_field(name="-", value=f"{character_name} hit their head on the way down, luckily, {character_name} didn't fall far\n-{hp_lost}%hp", inline=False)
                if cliff_scenario == 8 or cliff_scenario == 9:
                    energy_stones_gained = 3
                    embed.add_field(name="-", value=f"{character_name} caught a tree branch just in time and found some energy stones in the wall\n+{energy_stones_gained} energy stones", inline=False)
                if cliff_scenario == 10:
                    xp_gained = xp_suppresion(100, user_id)
                    energy_stones_gained = 20
                    embed.add_field(name="-", value=f"{character_name} found the cave of a forgotten warrior\n+{xp_gained}xp +{energy_stones_gained} energy stones", inline=False)
                    # first world key ----------------------------------------------------------------------------------------------------------------------------------------------------------------
                    if character_level > 9:
                        embed.add_field(name="-", value=f"{character_name} hears a deep voice coming from behind them, 'You no longer belong here, leave'. After turning around {character_name} sees nothing...", inline=False)
                        if stat_world_keys == 0:
                            embed.add_field(name="-", value=f"{character_name} understands that there's somewhere that they need to go, they can feel pressure holding them back\n+1 Englightenment", inline=False)
                            world_lock(1, stat_world_keys, user_id)

            if exploration_number == 2:
                energy_stones_gained = 1
                embed.add_field(name="-", value=f"{character_name} found an energy crystal in cave while passing by\n+{energy_stones_gained} energy stones", inline=False)

            if exploration_number == 3:
                embed.add_field(name="-", value=f"{character_name} was ambushed by a group of goblins", inline=False)
                lose_chance = random.randint(1,5)
                if lose_chance > character_level:
                    run_chance = random.randint(1,5)
                    if run_chance <= character_level:
                        embed.add_field(name="-", value=f"{character_name} got away", inline=False)
                    else:
                        hp_lost = hp_suppresion(30, user_id)
                        xp_gained = xp_suppresion(10, user_id)
                        embed.add_field(name="-", value=f"{character_name} was defeated, but {character_name} took one down with them\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                else:
                    hp_lost = hp_suppresion(5, user_id)
                    xp_gained = xp_suppresion(30, user_id)
                    embed.add_field(name="-", value=f"{character_name} sent those goblins to the underworld, {character_name} was scratched\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

            if exploration_number == 4:
                energy_stones_gained = 5
                embed.add_field(name="-", value=f"{character_name} saw a passing merchant and after selling off a strange stick {character_name} found, the merchant gave {character_name} some energy stones\n+{energy_stones_gained} energy stones", inline=False)
            
            if exploration_number == 5:
                energy_stones_gained = random.randint(1,3)
                embed.add_field(name="-", value=f"Walking along the dirt road, a migrant tripped and dropped {energy_stones_gained} energy stone(s)... {character_name}'s lucky day\n+{energy_stones_gained} energy stones", inline=False)

            if exploration_number == 6:
                embed.add_field(name="-", value=f"A group of thugs passing by starts harassing {character_name}", inline=False)
                lose_chance = random.randint(1,10)
                if lose_chance > character_level:
                    hp_lost = hp_suppresion(40, user_id)
                    xp_gained = xp_suppresion(5, user_id)
                    embed.add_field(name="-", value=f"They couldn't find anything valuable on {character_name}, so they beat {character_name} up\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                else:
                    energy_stones_gained = 3
                    hp_lost = hp_suppresion(10, user_id)
                    xp_gained = xp_suppresion(50, user_id)
                    embed.add_field(name="-", value=f"{character_name} beat them within an inch of their lives\n+{energy_stones_gained} energy stones -{hp_lost}%hp +{xp_gained}xp", inline=False)

            if exploration_number == 7:
                embed.add_field(name="-", value=f"{character_name} sees an old lady being yelled at by a middle aged man and she starts crying", inline=False)
                ladyEncounter = random.randint(1,2)
                if ladyEncounter == 1:
                    hp_lost = hp_suppresion(10, user_id)
                    xp_gained = xp_suppresion(15, user_id)
                    embed.add_field(name="-", value=f"{character_name} decided to get into a fight with the middle aged man and beats him up, only to hear about his speech impediment and that he was trying to cheer her up\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                elif ladyEncounter == 2:
                    embed.add_field(name="-", value=f"{character_name} ignores the yelling thinking that it's just part of human nature", inline=False)

            if exploration_number == 8:
                energy_stones_gained = random.randint(10,25)
                embed.add_field(name="-", value=f"An enemy of a rich family decimates the family's home, leaving their treasury scattered across the ground\n+{energy_stones_gained} energy stones", inline=False)

            if exploration_number == 9:
                xp_gained = xp_suppresion(10, user_id)
                embed.add_field(name="-", value=f"A famous warrior walked into an inn {character_name} was staying at and tripped, they walk out after telling you never to wear high heels, to wear something comfortable\n+{xp_gained}xp", inline=False)

            if exploration_number == 10:
                xp_gained = xp_suppresion(15, user_id)
                embed.add_field(name="-", value=f"{character_name} found a caravan to join; after the trip {character_name} learned a lot\n+{xp_gained}xp", inline=False)

            if exploration_number == 11:
                forst_weeks_spent = random.randint(1,3)
                xp_gained = xp_suppresion(forst_weeks_spent * 7, user_id)
                embed.add_field(name="-", value=f"{character_name} spent {forst_weeks_spent} weeks in the woods\n+{xp_gained}xp", inline=False)

            if exploration_number == 12:
                embed.add_field(name="-", value=f"{character_name} participated in a nearby tournament", inline=False)
                hp_lost = hp_suppresion(random.randint(10,50), user_id)
                first_round_odds = random.randint(1,5)
                second_round_odds = random.randint(3,7)
                quarter_final_odds = random.randint(5,8)
                semi_final_odds = random.randint(6,9)
                final_odds = random.randint(7,10)

                if character_level >= final_odds:
                                    xp_gained = xp_suppresion(100, user_id)
                                    embed.add_field(name="-", value=f"{character_name} was the **Champion**\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character_level >= semi_final_odds:
                                xp_gained = xp_suppresion(80, user_id)
                                embed.add_field(name="-", value=f"{character_name} won the semi finals\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character_level >= quarter_final_odds:
                            xp_gained = xp_suppresion(60, user_id)
                            embed.add_field(name="-", value=f"{character_name} won the quarter finals\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character_level >= second_round_odds:
                        xp_gained = xp_suppresion(40, user_id)
                        embed.add_field(name="-", value=f"{character_name} won the second round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character_level >= first_round_odds:
                    xp_gained = xp_suppresion(20, user_id)
                    embed.add_field(name="-", value=f"{character_name} won the first round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                else:
                    xp_gained = xp_suppresion(10, user_id)
                    embed.add_field(name="-", value=f"{character_name} lost in the first round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

            # second world key ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if exploration_number == 13:
                xp_gained = xp_suppresion(25, user_id)
                if character_level > 9:
                    embed.add_field(name="-", value=f"A wrinkled old man passed by {character_name} while preeching about the frustrations of mortals, {character_name} feels enlightened\n+{xp_gained}xp", inline=False)
                    if stat_world_keys == 1:
                            embed.add_field(name="-", value=f"{character_name} knows that they've broken the shackles of mortality and they need to go to new heights.\n+1 Englightenment", inline=False)
                            world_lock(2, stat_world_keys, user_id)
                else:
                    embed.add_field(name="-", value=f"A wrinkled old man passed by {character_name} while muttering something incomprehensible, {character_name} feels enlightened\n+{xp_gained}xp", inline=False)

            if exploration_number == 14:
                embed.add_field(name="-", value=f"{character_name} found a cave with a light shining through some vines", inline=False)
                cave_occupant_odds = random.randint(1,5)

                if cave_occupant_odds == 1:
                    embed.add_field(name="-", value=f"The occupant doesn't appreciate {character_name}'s snooping and attacks you", inline=False)
                    withstand_chance = random.randint(5,7)

                    if character_level >= withstand_chance:
                        energy_stones_gained = 33
                        hp_lost = hp_suppresion(5, user_id)
                        embed.add_field(name="-", value=f"{character_name} was caught off guard but withstood the attack, {character_name} was going to ask why they did that but discovered the occupant disappeared so {character_name} looted their home for compensation for you chest pain\n-{hp_lost}%hp +{energy_stones_gained} energy stones", inline=False)

                    else:
                        hp_lost = hp_suppresion(20, user_id)
                        embed.add_field(name="-", value=f"{character_name} realizes too late that there is excess energy in their body and blacks out only to wake up in the middle of the forest\n-{hp_lost}%hp", inline=False)

                else:
                    embed.add_field(name="-", value=f"Seems like no one is there, oh well", inline=False)

            # third world key --------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if exploration_number == 15:
                if not character_level > 9:
                    hp_lost = hp_suppresion(10, user_id)
                embed.add_field(name="-", value=f"A snow dragon warrior flew over {character_name} during their travels, it's a little cold\n-{hp_lost}%hp", inline=False)
                if stat_world_keys == 2:
                            embed.add_field(name="-", value=f"{character_name} follows the dragon warrior, finds that they've travelled through a portal. I wonder where this leads.\n+1 Englightenment", inline=False)
                            world_lock(3, stat_world_keys, user_id)

            if exploration_number == 16:
                gender = random.randint(1,2)
                if gender == 1:
                    gender = "boy"
                else:
                    gender = "girl"
                xp_gained = xp_suppresion(10, user_id)
                embed.add_field(name="-", value=f"{character_name} watches as a young {gender} gets killed in a fight for resources, poor thing\n+{xp_gained}xp", inline=False)

            if exploration_number == 17:
                energy_stones_gained = random.randint(3,10)
                embed.add_field(name="-", value=f"{character_name} found a collector who collects well shaped energy stones, {character_name} pulls out their very best stone and sells it to him\n+{energy_stones_gained} energy stones", inline=False)

            if exploration_number == 18:
                hp_lost = hp_suppresion(5, user_id)
                embed.add_field(name="-", value=f"{character_name} was resting on a tree in a forest, a fairy flew by and scared {character_name} off the tree, ouch\n-{hp_lost}%hp", inline=False)

            if exploration_number == 19:
                xp_gained = xp_suppresion(15, user_id)
                embed.add_field(name="-", value=f"{character_name} passes by a nearby valley and learns about the history from a guide, there used to be 2 unique races here but they mutually destroyed themselves…\n+{xp_gained}xp", inline=False)

            if exploration_number == 20:
                xp_gained = xp_suppresion(5, user_id)
                embed.add_field(name="-", value=f"{character_name} passed by a seemingly ordinary tree that begins talking about it's day with {character_name}... weird\n+{xp_gained}xp", inline=False)

            if exploration_number == 21:
                embed.add_field(name="-", value=f"During {character_name}'s travels they encounter a group of undercover demons", inline=False)
                capture_odds = random.randint(3,7)
                if capture_odds >= character_level:
                    hp_lost = hp_suppresion(15, user_id)
                    embed.add_field(name="-", value=f"{character_name} was captured, after being set free {character_name}'s head feels fuzzy\n-{hp_lost}hp", inline=False)
                else:
                    fight_odds = random.randint(7,10)
                    if fight_odds <= character_level:
                        xp_gained = xp_suppresion(50, user_id)
                        hp_lost = hp_suppresion(random.randint(5,15), user_id)
                        embed.add_field(name="-", value=f"{character_name} beat up the demons and found that they plan on taking over the nearby area, interesting\n-{hp_lost}hp +{xp_gained}xp", inline=False)
                    else:
                        embed.add_field(name="-", value=f"{character_name} fled and after being chased for awhile, {character_name} came upon a town and realized the demons disappeared.", inline=False)

            if exploration_number == 22:
                embed.add_field(name="-", value=f"{character_name} found a castle in the middle of nowhere, {character_name} travelled here after learning about it's invinciblity in a nearby inn.", inline=False)
                if not character_level >= 30:
                    hp_lost = hp_suppresion(5, user_id)
                    embed.add_field(name="-", value=f"{character_name} tries to punch the wall, ouch\n-{hp_lost}%hp", inline=False)
                else:
                    embed.add_field(name="-", value=f"The wall shatters, huh...", inline=False)

            if exploration_number == 23:
                hp_lost = hp_suppresion(5, user_id)
                energy_stones_gained = 10
                embed.add_field(name="-", value=f"A person appears infront of {character_name}, slaps {character_name} and disappears... they wonder why that happened until they find that they feel sick.\n-{hp_lost}%hp +{energy_stones_gained} energy stones", inline=False)

            if exploration_number == 24:
                xp_gained = xp_suppresion(15, user_id)
                embed.add_field(name="-", value=f"{character_name} finds a group of people, dancing on a hill. They join in on the fun, how exhilerating!\n+{xp_gained}xp", inline=False)

            if exploration_number == 25:
                embed.add_field(name="-", value=f"During {character_name}'s travels they encounter a person that starts saying that they're possessed", inline=False)
                
                fight_odds = random.randint(3,7)
                if character_level >= fight_odds:
                    xp_gained = xp_suppresion(35, user_id)
                    hp_lost = hp_suppresion(10, user_id)
                    embed.add_field(name="-", value=f"The person attacks you, you successfully defended yourself.\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

                else:
                    hp_lost = hp_suppresion(10, user_id)
                    embed.add_field(name="-", value=f"The person attacks you, you were beaten up.\n-{hp_lost}%hp", inline=False)
                    
        elif character_world_level == 2:
            if exploration_number == 1:
                pass
        
        character_update(hp_lost, xp_gained, energy_stones_gained, user_id)

        dead = death_check(hp_lost, user_id)
        if dead:
            embed.add_field(name=f"Character Death", value=f"{character_name} died, but they don't know that they've died.", inline=False)

        await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.command()
    async def stats(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        user_id = ctx.author.id
        channel = self.bot.get_channel(969009985512157194)
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name FROM incremental WHERE user_id = ?', (user_id,))
            character_name = cursor.fetchone()
            character_name = character_name[0]
            cursor.execute(f'SELECT stat_explorations FROM incremental WHERE user_id = ?', (user_id,))
            stat_explorations = cursor.fetchone()
            stat_explorations = stat_explorations[0]
            cursor.execute(f'SELECT stat_damage_taken FROM incremental WHERE user_id = ?', (user_id,))
            stat_damage_taken = cursor.fetchone()
            stat_damage_taken = stat_damage_taken[0]
            cursor.execute(f'SELECT stat_xp_gained FROM incremental WHERE user_id = ?', (user_id,))
            stat_xp_gained = cursor.fetchone()
            stat_xp_gained = stat_xp_gained[0]
            cursor.execute(f'SELECT stat_energy_stones_gained FROM incremental WHERE user_id = ?', (user_id,))
            stat_energy_stones_gained = cursor.fetchone()
            stat_energy_stones_gained = stat_energy_stones_gained[0]
            cursor.execute(f'SELECT stat_birthday FROM incremental WHERE user_id = ?', (user_id,))
            stat_birthday = cursor.fetchone()
            stat_birthday = stat_birthday[0]
            if stat_birthday == 1651019868:
                stat_birthday = "The Primordial Era"
            else:
                stat_birthday = f"<t:{stat_birthday}:d>"
            stat_xp_gained = number_format(stat_xp_gained)
            stat_explorations = number_format(stat_explorations)
            stat_damage_taken = number_format(stat_damage_taken)
            stat_energy_stones_gained = number_format(stat_energy_stones_gained)
            
        embed = discord.Embed(description="", colour=0x800080, timestamp=datetime.utcnow())
        embed.set_author(name=character_name, icon_url=ctx.author.display_avatar)
        embed.add_field(name="Total Explorations:", value=f"{stat_explorations}", inline=False)
        embed.add_field(name="Total Damage Taken:", value=f"{stat_damage_taken}", inline=False)
        embed.add_field(name="Total Experience Gained", value=f"{stat_xp_gained}", inline=False)
        embed.add_field(name="Total energy stones Gained", value=f"{stat_energy_stones_gained}", inline=False)
        embed.add_field(name="Character's Birthday", value=f"{stat_birthday}", inline=False)
        await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.command()
    async def rankings(self, ctx: commands.Context):
        character = character_check(ctx.author.id)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await ctx.send(embed=embed)
            return
        channel = self.bot.get_channel(969009985512157194)
        user_id = ctx.author.id
        with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT character_name, character_level, character_xp FROM incremental GROUP BY character_name ORDER BY 2 DESC, 3 DESC LIMIT 10")
            lb = cursor.fetchall()
            cursor.execute(f"SELECT character_name, character_level, character_xp FROM incremental WHERE user_id = ?", (user_id,))
            rank = cursor.fetchone()
        embed = discord.Embed(title="Advancement Rankings", description=f":first_place: **{lb[0][0]}** Level: {lb[0][1]} XP: {lb[0][2]}\n:second_place: **{lb[1][0]}** Level: {lb[1][1]} XP: {lb[1][2]}\n:third_place: **{lb[2][0]}** Level: {lb[2][1]} XP: {lb[2][2]}\n:medal: **{lb[3][0]}** Level: {lb[3][1]} XP: {lb[3][2]}\n:medal: **{lb[4][0]}** Level: {lb[4][1]} XP: {lb[4][2]}\n:medal: **{lb[5][0]}** Level: {lb[5][1]} XP: {lb[5][2]}\n:medal: **{lb[6][0]}** Level: {lb[6][1]} XP: {lb[6][2]}\n:medal: **{lb[7][0]}** Level: {lb[7][1]} XP: {lb[7][2]}\n:medal: **{lb[8][0]}** Level: {lb[8][1]} XP: {lb[8][2]}\n:medal: **{lb[9][0]}** Level: {lb[9][1]} XP: {lb[9][2]}\n\nYour character:\n**{rank[0]}** Level: {rank[1]} XP: {rank[2]}", colour=0x800080, timestamp=datetime.utcnow())
        await ctx.send(embed=embed); await channel.send(embed=embed)

    @commands.Cog.listener() # Message logger
    async def on_message(self, message: discord.Message):
        if not message.guild == None:
            return
        if message.content.startswith('-'):
            return
        if message.content == '':
            return
        channel = self.bot.get_channel(969009985512157194)
        embed = discord.Embed(description=f"**Message from {message.author} in Essence Bot DMS**:\n{message.content}", colour=0x800080)
        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    print("Incremental Cog Ready")
    await bot.add_cog(Incremental(bot))