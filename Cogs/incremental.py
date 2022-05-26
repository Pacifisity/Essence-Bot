import discord
import sqlite3
import random
from discord.ext import commands
from datetime import datetime
from discord import app_commands


class Database():
    def __init__(self):
        with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
            cursor = db.cursor()
            self.cursor = cursor
            self.db = db


class Character():
    def __init__(self, member):
        self.member = member
        self.id = member.id
        with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
            cursor = db.cursor()

            attributes = [
                "member_id",
                "character_name",
                "character_level",
                "character_energy_stones",
                "character_world_level",
                "character_xp",
                "character_xp_required",
                "character_hp",
                "stat_birthday",
                "stat_world_boss_damage",
                "stat_explorations",
                "stat_world_keys",
                "stat_damage_taken",
                "stat_xp_gained",
                "stat_energy_stones_gained",
                "cooldown_character_name",
                "cooldown_rest"
            ]

            with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
                cursor = db.cursor()
                for attribute in attributes:
                    cursor.execute(
                        f'SELECT {attribute} FROM incremental WHERE member_id = ?', (member.id,))
                    fetched_value = cursor.fetchone()
                    setattr(self, attribute, fetched_value[0])

    def information(self):
        return [self.character_name, self.character_level, self.character_energy_stones, self.character_world_level, self.character_xp, self.character_xp_required, self.character_hp]

    def stats(self):
        return [self.stat_birthday, self.stat_world_boss_damage, self.stat_explorations, self.stat_world_keys, self.stat_damage_taken, self.stat_xp_gained, self.stat_energy_stones_gained]


def number_format(number):
    number = "{:,}".format(number)
    return number


def hp_suppresion(hp_lost, member):
    character = Character(member)

    max_world_level = 10 * character.character_world_level
    if character.character_level > max_world_level:
        hp_lost = (
            hp_lost / (1 + ((character.character_level - max_world_level) / 10)))
        if character.character_level > max_world_level + 10:
            hp_lost = hp_lost / 3 * \
                (1 + ((character.character_level - max_world_level) / 10))

    hp_randomizer = random.randint(1, 3)
    hp_lost = hp_lost * (0.8 + (hp_randomizer / 10))

    return int(hp_lost)


def xp_suppresion(xp_gained, member):
    character = Character(member)

    max_world_level = 10 * character.character_world_level
    if character.character_level > max_world_level:
        xp_gained = xp_gained / \
            (1 + ((character.character_level - max_world_level) / 10))
        if character.character_level > max_world_level + 10:
            xp_gained = xp_gained / 3 * \
                (1 + ((character.character_level - max_world_level) / 10))

    xp_randomizer = random.randint(1, 3)
    xp_gained = xp_gained * (0.8 + xp_randomizer / 10)

    return int(xp_gained)


def character_update(hp_lost, xp_gained, energy_stones_gained, member):
    character = Character(member)
    database = Database()

    sql = "UPDATE incremental SET character_xp = ?, character_hp = ?, character_energy_stones = ? WHERE member_id = ?"
    val = ((character.character_xp + xp_gained), (character.character_hp - hp_lost),
           (character.character_energy_stones + energy_stones_gained), member.id)
    database.cursor.execute(sql, val)
    database.db.commit()

    sql = "UPDATE incremental SET stat_explorations = ?, stat_xp_gained = ?, stat_damage_taken = ?, stat_energy_stones_gained = ? WHERE member_id = ?"
    val = ((character.stat_explorations + 1), (character.stat_xp_gained + xp_gained),
           (character.stat_damage_taken + hp_lost), (character.stat_energy_stones_gained + energy_stones_gained), member.id)
    database.cursor.execute(sql, val)
    database.db.commit()


def death_check(hp_lost, member):
    character = Character(member)
    database = Database()

    if character.character_hp <= 0:
        if round(character.character_xp - character.character_xp_required * 0.2) <= 0:
            experience_after_death = 0
        else:
            experience_after_death = round(
                character.character_xp - character.character_xp_required * 0.2)

        character_hp = character.character_hp + hp_lost

        sql = "UPDATE incremental SET character_xp = ?, character_hp = ? WHERE member_id = ?"
        val = (experience_after_death, character_hp, member.id)
        database.cursor.execute(sql, val)
        database.db.commit()
        dead = True
    else:
        dead = False
    return dead


def world_lock(unlock_scenario, stat_world_keys, member):
    with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
        cursor = db.cursor()
    if unlock_scenario == 1:
        if stat_world_keys == 0:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE member_id = ?"
            val = (1, member.id)
    elif unlock_scenario == 2:
        if stat_world_keys == 1:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE member_id = ?"
            val = (2, member.id)
    elif unlock_scenario == 3:
        if stat_world_keys == 2:
            sql = "UPDATE incremental SET stat_world_keys = ? WHERE member_id = ?"
            val = (3, member.id)
    else:
        sql = "UPDATE incremental SET stat_world_keys = ? WHERE member_id = ?"
        val = (stat_world_keys, member.id)
    cursor.execute(sql, val)
    db.commit()


def default_embed(title=None, description=None, member=None):
    if title == None:
        embed = discord.Embed(description=description, color=0x800080)
    if description == None:
        embed = discord.Embed(title=title, color=0x800080)
    else:
        embed = discord.Embed(
            title=title, description=description, color=0x800080)
    if member != None:
        embed.set_author(name=member.name, icon_url=member.display_avatar)
    return embed


class Incremental(commands.Cog, app_commands.Group):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.incremental_logs = self.bot.get_channel(969009985512157194)
        self.timestamp = round(datetime.now().timestamp())
        super().__init__()

    async def send_message(self, interaction: discord.Interaction, embed):
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.incremental_logs.send(embed=embed)

    @app_commands.command(name="patch")
    async def patch(self, interaction: discord.Interaction, week: str = None):
        member = interaction.user
        if week == None:
            week = "2"
        with open(f'DB Storage\patchNotes\patch{week}.txt') as patch:
            embed = default_embed(description=patch.read(), member=member)
            await self.send_message(interaction, embed)

    @app_commands.command()
    async def register(self, interaction: discord.Interaction, *, character_name: str = None):
        member = interaction.user
        timestamp = round(datetime.now().timestamp())
        character = Character(member)
        database = Database()
        if character.character_name == None:
            if not character.character_name == None:
                embed = default_embed(
                    f"You've already started your journey, {character.character_name}", member=member)
                await self.send_message(interaction, embed)
            else:
                embed = default_embed(f"To begin your journey, please register your character's name '$register (character name)'\n\nWelcome to the game of Essence, story based incremental rpg. In Essence you take control of a character born from Energy, plopped down in the middle of nowhere and with a multitude of scenarios to '$explore'.", member=member)
                await self.send_message(interaction, embed)
        else:
            if character.character_name == None:
                sql = "INSERT INTO incremental(member_id, character_name, character_level, character_energy_stones, character_world_level, character_xp, character_xp_required, character_hp, stat_birthday, stat_explorations, stat_damage_taken, stat_xp_gained, stat_energy_stones_gained, stat_world_boss_damage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val = (member.id, character_name, 1, 0, 1,
                       0, 100, 100, timestamp, 0, 0, 0, 0, 0)
                database.cursor.execute(sql, val)
                database.db.commit()
                embed = default_embed(
                    f"Welcome to the game of Essence, your character {character_name} has been created.", member=member)
                await self.send_message(interaction, embed)
            else:
                embed = default_embed(
                    f"You've already started your journey, {character_name[0]}", member=member)
                await self.send_message(interaction, embed)

    @app_commands.command()
    async def character(self, interaction: discord.Interaction):
        member = interaction.user
        character = Character(member)
        if character.character_name == None:
            embed = discord.Embed(
                description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await self.send_message(interaction, embed)
            return

        if character.character_level <= 9:
            state_of_being = "Mortal"
        if character.character_level >= 10 and character.character_level <= 59:
            state_of_being = "Warrior"
        if character.character_level >= 60 and character.character_level <= 99:
            state_of_being = "Immortal"
        if character.character_level >= 100:
            state_of_being = "God"
        character_xp = number_format(character.character_xp)
        character_xp_required = number_format(character.character_xp_required)
        character_energy_stones = number_format(
            character.character_energy_stones)

        embed = default_embed(f"Character Information:", member=member)
        embed.add_field(
            name="Name", value=f"{character.character_name}", inline=True)
        embed.add_field(
            name="Level", value=f"{state_of_being} {character.character_level}", inline=True)
        embed.add_field(
            name="Experience", value=f"{character_xp} of {character_xp_required}", inline=True)
        embed.add_field(
            name="Health", value=f"{character.character_hp}%", inline=True)
        embed.add_field(name="Energy Stones",
                        value=f"{character_energy_stones}", inline=True)
        await self.send_message(interaction, embed)

    @app_commands.command()
    async def advance(self, interaction: discord.Interaction):
        member = interaction.user
        character = Character(member)
        database = Database()
        if character.character_name == None:
            embed = default_embed(
                "You don't have a character yet, do '$register (character name)' to create a character!", member=member)
            await self.send_message(embed)
            return
        if character.character_level <= 9:
            state_of_being = "Mortal"
        elif character.character_level <= 59 and character.character_level >= 10:
            state_of_being = "Warrior"
        elif character.character_level <= 99 and character.character_level >= 60:
            state_of_being = "Immortal"
        elif character.character_level >= 100:
            state_of_being = "God"
        if character.character_xp >= character.character_xp_required:
            embed = default_embed(
                f"{character.character_name} has advanced to {state_of_being} {character.character_level + 1}!", member=member)
            sql = "UPDATE incremental SET character_level = ?, character_xp = ?, character_xp_required = ? WHERE member_id = ?"
            val = (character.character_level + 1, 0,
                   round(character.character_xp_required * 1.35), member.id)
            database.cursor.execute(sql, val)
            database.db.commit()
            await self.send_message(interaction, embed)
        else:
            embed = default_embed(
                f"{character.character_name} wasn't ready to advance and caused a backlash on their mind while trying.\n-10hp", member=member)
            sql = "UPDATE incremental SET character_hp = ? WHERE member_id = ?"
            val = (character.character_hp - 10, member.id)
            database.cursor.execute(sql, val)
            database.db.commit()
            await self.send_message(interaction, embed)

        dead = death_check(10, member)
        if dead:
            embed = default_embed(
                f"{character.character_name} died while trying to advance, they feel weaker but they don't remember dying", member=member)
            await self.send_message(interaction, embed)

    """
    @app_commands.command()
    async def world(self, interaction: discord.Interaction, number: int = 1):
        member = interaction.user
        member_id = member.id
        character = character_check(member)
        if not character:
            embed = discord.Embed(description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT character_name, character_world_level, stat_world_keys FROM incremental WHERE member_id = ?', (member_id,))
            character_information = cursor.fetchone()
            character_name = character_information[0]
            character_world_level = character_information[1]
            stat_world_keys = character_information[2]
            if character_world_level == number:
                embed = discord.Embed(description=f"{character_name} decided they want to go somewhere today, but they're not sure where.", colour=0x800080)
                await self.send_message(interaction, embed)
                return
            if character_world_level == 1:
                if stat_world_keys >= 3:
                    embed = discord.Embed(description=f"{character_name} steps close to the portal, they feel a pull. As they walk closer to the portal a faint pressure can be felt. The pressure is no sweat for {character_name} and they walk into the portal.", colour=0x800080)
                    sql = "UPDATE incremental SET character_world_level = ? WHERE member_id = ?"
                    val = (2, member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    await self.send_message(interaction, embed)
            if character_world_level == 2:
                embed = discord.Embed(description=f"{character_name} travels back to the point where they first entered this world, and steps back through the portal.", colour=0x800080)
                sql = "UPDATE incremental SET character_world_level = ? WHERE member_id = ?"
                val = (1, member.id)
                cursor.execute(sql, val)
                db.commit()
                await self.send_message(interaction, embed)
    """

    @app_commands.command()
    async def recover(self, interaction: discord.Interaction):
        member = interaction.user
        timestamp = round(datetime.now().timestamp())
        character = Character(member)
        database = Database()
        if character.character_name == None:
            embed = default_embed(
                "You don't have a character yet, do '$register (character name)' to create a character!", member=member)
            await self.send_message(embed)
            return
        if character.cooldown_rest == None or character.cooldown_rest <= timestamp - 3600:
            embed = default_embed(f"You have fully recovered!", member=member)
            sql = "UPDATE incremental SET character_hp = ?, cooldown_rest = ? WHERE member_id = ?"
            val = (100, timestamp, member.id)
            database.cursor.execute(sql, val)
            database.db.commit()
        else:
            embed = default_embed(
                f"Too much recovery at once could affect the healing process. You can recover again <t:{character.cooldown_rest + 3600}:R>", member=member)
        await self.send_message(interaction, embed)

    @app_commands.command()
    async def explore(self, interaction: discord.Interaction):
        member = interaction.user
        character = Character(member)
        if character.character_name == None:
            embed = default_embed(
                "You don't have a character yet, do '$register (character name)' to create a character!", member=member)
            await self.send_message(embed)
            return
        exploration_number = random.randint(1, 25)

        if character.stat_world_keys == None:
            character.stat_world_keys = 0
        hp_lost = 0
        xp_gained = 0
        energy_stones_gained = 0

        embed = default_embed(
            f"**{character.character_name} went on an adventure to explore the world of Essence**", member=member)
        if character.character_world_level == 1:

            if exploration_number == 1:
                embed.add_field(
                    name="-", value=f"{character.character_name} fell down a cliff", inline=False)
                cliff_scenario = random.randint(1, 10)
                if cliff_scenario <= 7:
                    hp_lost = hp_suppresion(5, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} hit their head on the way down, luckily, {character.character_name} didn't fall far\n-{hp_lost}%hp", inline=False)
                if cliff_scenario == 8 or cliff_scenario == 9:
                    energy_stones_gained = 3
                    embed.add_field(
                        name="-", value=f"{character.character_name} caught a tree branch just in time and found some energy stones in the wall\n+{energy_stones_gained} Energy Stones", inline=False)
                if cliff_scenario == 10:
                    xp_gained = xp_suppresion(100, member)
                    energy_stones_gained = 20
                    embed.add_field(
                        name="-", value=f"{character.character_name} found the cave of a forgotten warrior\n+{xp_gained}xp +{energy_stones_gained} Energy Stones", inline=False)
                    # first world key ----------------------------------------------------------------------------------------------------------------------------------------------------------------
                    if character.character.character_level > 9:
                        embed.add_field(
                            name="-", value=f"{character.character_name} hears a deep voice coming from behind them, 'You no longer belong here, leave'. After turning around {character.character_name} sees nothing...", inline=False)
                        if character.stat_world_keys == 0:
                            embed.add_field(
                                name="-", value=f"{character.character_name} understands that there's somewhere that they need to go, they can feel pressure holding them back\n+1 Englightenment", inline=False)
                            world_lock(1, character.stat_world_keys)

            if exploration_number == 2:
                energy_stones_gained = 1
                embed.add_field(
                    name="-", value=f"{character.character_name} found an energy crystal in cave while passing by\n+{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 3:
                embed.add_field(
                    name="-", value=f"{character.character_name} was ambushed by a group of goblins", inline=False)
                lose_chance = random.randint(1, 5)
                if lose_chance > character.character_level:
                    run_chance = random.randint(1, 5)
                    if run_chance <= character.character_level:
                        embed.add_field(
                            name="-", value=f"{character.character_name} got away", inline=False)
                    else:
                        hp_lost = hp_suppresion(30, member)
                        xp_gained = xp_suppresion(10, member)
                        embed.add_field(
                            name="-", value=f"{character.character_name} was defeated, but {character.character_name} took one down with them\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                else:
                    hp_lost = hp_suppresion(5, member)
                    xp_gained = xp_suppresion(30, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} sent those goblins to the underworld, {character.character_name} was scratched\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

            if exploration_number == 4:
                energy_stones_gained = 5
                embed.add_field(
                    name="-", value=f"{character.character_name} saw a passing merchant and after selling off a strange stick {character.character_name} found, the merchant gave {character.character_name} some energy stones.\n+{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 5:
                energy_stones_gained = random.randint(1, 3)
                embed.add_field(
                    name="-", value=f"Walking along the dirt road, a migrant tripped and dropped {energy_stones_gained} energy stone(s)... {character.character_name}'s lucky day\n+{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 6:
                embed.add_field(
                    name="-", value=f"A group of thugs passing by starts harassing {character.character_name}", inline=False)
                lose_chance = random.randint(1, 10)
                if lose_chance > character.character_level:
                    hp_lost = hp_suppresion(40, member)
                    xp_gained = xp_suppresion(5), member
                    embed.add_field(
                        name="-", value=f"They couldn't find anything valuable on {character.character_name}, so they beat {character.character_name} up\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                else:
                    energy_stones_gained = 3
                    hp_lost = hp_suppresion(10, member)
                    xp_gained = xp_suppresion(50, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} beat them within an inch of their lives\n+{energy_stones_gained} Energy Stones -{hp_lost}%hp +{xp_gained}xp", inline=False)

            if exploration_number == 7:
                embed.add_field(
                    name="-", value=f"{character.character_name} sees an old lady being yelled at by a middle aged man and she starts crying", inline=False)
                ladyEncounter = random.randint(1, 2)
                if ladyEncounter == 1:
                    hp_lost = hp_suppresion(10, member)
                    xp_gained = xp_suppresion(15, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} decided to get into a fight with the middle aged man and beats him up, only to hear about his speech impediment and that he was trying to cheer her up\n-{hp_lost}%hp +{xp_gained}xp", inline=False)
                elif ladyEncounter == 2:
                    embed.add_field(
                        name="-", value=f"{character.character_name} ignores the yelling thinking that it's just part of human nature", inline=False)

            if exploration_number == 8:
                energy_stones_gained = random.randint(10, 25)
                embed.add_field(
                    name="-", value=f"An enemy of a rich family decimates the family's home, leaving their treasury scattered across the ground\n+{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 9:
                xp_gained = xp_suppresion(10, member)
                embed.add_field(
                    name="-", value=f"A famous warrior walked into an inn {character.character_name} was staying at and tripped, they walk out after telling you never to wear high heels, to wear something comfortable\n+{xp_gained}xp", inline=False)

            if exploration_number == 10:
                xp_gained = xp_suppresion(15, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} found a caravan to join; after the trip {character.character_name} learned a lot\n+{xp_gained}xp", inline=False)

            if exploration_number == 11:
                forest_weeks_spent = random.randint(1, 3)
                xp_gained = xp_suppresion(forest_weeks_spent * 7, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} spent {forest_weeks_spent} weeks in the woods\n+{xp_gained}xp", inline=False)

            if exploration_number == 12:
                embed.add_field(
                    name="-", value=f"{character.character_name} participated in a nearby tournament", inline=False)
                hp_lost = hp_suppresion(random.randint(10, 50), member)
                first_round_odds = random.randint(1, 5)
                second_round_odds = random.randint(3, 7)
                quarter_final_odds = random.randint(5, 8)
                semi_final_odds = random.randint(6, 9)
                final_odds = random.randint(7, 10)

                if character.character_level >= final_odds:
                    xp_gained = xp_suppresion(10, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} was the **Champion**\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character.character_level >= semi_final_odds:
                    xp_gained = xp_suppresion(80, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} won the semi finals\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character.character_level >= quarter_final_odds:
                    xp_gained = xp_suppresion(60, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} won the quarter finals\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character.character_level >= second_round_odds:
                    xp_gained = xp_suppresion(40, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} won the second round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                elif character.character_level >= first_round_odds:
                    xp_gained = xp_suppresion(20, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} won the first round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)
                else:
                    xp_gained = xp_suppresion(10, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} lost in the first round\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

            # second world key ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if exploration_number == 13:
                xp_gained = xp_suppresion(25, member)
                if character.character_level > 9:
                    embed.add_field(
                        name="-", value=f"A wrinkled old man passed by {character.character_name} while preeching about the frustrations of mortals, {character.character_name} feels enlightened\n+{xp_gained}xp", inline=False)
                    if character.stat_world_keys == 1:
                        embed.add_field(
                            name="-", value=f"{character.character_name} knows that they've broken the shackles of mortality and they need to go to new heights.\n+1 Englightenment", inline=False)
                        world_lock(2, character.stat_world_keys)
                else:
                    embed.add_field(
                        name="-", value=f"A wrinkled old man passed by {character.character_name} while muttering something incomprehensible, {character.character_name} feels enlightened\n+{xp_gained}xp", inline=False)

            if exploration_number == 14:
                embed.add_field(
                    name="-", value=f"{character.character_name} found a cave with a light shining through some vines", inline=False)
                cave_occupant_odds = random.randint(1, 5)

                if cave_occupant_odds == 1:
                    embed.add_field(
                        name="-", value=f"The occupant doesn't appreciate {character.character_name}'s snooping and attacks you", inline=False)
                    withstand_chance = random.randint(5, 7)

                    if character.character_level >= withstand_chance:
                        energy_stones_gained = 33
                        hp_lost = hp_suppresion(5, member)
                        embed.add_field(name="-", value=f"{character.character_name} was caught off guard but withstood the attack, {character.character_name} was going to ask why they did that but discovered the occupant disappeared so {character.character_name} looted their home for compensation for you chest pain\n-{hp_lost}%hp +{energy_stones_gained} Energy Stones", inline=False)

                    else:
                        hp_lost = hp_suppresion(20, member)
                        embed.add_field(
                            name="-", value=f"{character.character_name} realizes too late that there is excess energy in their body and blacks out only to wake up in the middle of the forest\n-{hp_lost}%hp", inline=False)

                else:
                    embed.add_field(
                        name="-", value=f"Seems like no one is there, oh well", inline=False)

            # third world key --------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if exploration_number == 15:
                if not character.character_level > 9:
                    hp_lost = hp_suppresion(10, member)
                embed.add_field(
                    name="-", value=f"A snow dragon warrior flew over {character.character_name} during their travels, it's a little cold\n-{hp_lost}%hp", inline=False)
                if character.stat_world_keys == 2:
                    embed.add_field(
                        name="-", value=f"{character.character_name} follows the dragon warrior, finds that they've travelled through a portal. I wonder where this leads.\n+1 Englightenment", inline=False)
                    world_lock(3, character.stat_world_keys)

            if exploration_number == 16:
                gender = random.randint(1, 2)
                if gender == 1:
                    gender = "boy"
                else:
                    gender = "girl"
                xp_gained = xp_suppresion(10, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} watches as a young {gender} gets killed in a fight for resources, poor thing\n+{xp_gained}xp", inline=False)

            if exploration_number == 17:
                energy_stones_gained = random.randint(3, 10)
                embed.add_field(
                    name="-", value=f"{character.character_name} found a collector who collects well shaped Energy Stones, {character.character_name} pulls out their very best stone and sells it to him\n+{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 18:
                hp_lost = hp_suppresion(5, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} was resting on a tree in a forest, a fairy flew by and scared {character.character_name} off the tree, ouch\n-{hp_lost}%hp", inline=False)

            if exploration_number == 19:
                xp_gained = xp_suppresion(15, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} passes by a nearby valley and learns about the history from a guide, there used to be 2 unique races here but they mutually destroyed themselves…\n+{xp_gained}xp", inline=False)

            if exploration_number == 20:
                xp_gained = xp_suppresion(5), member
                embed.add_field(
                    name="-", value=f"{character.character_name} passed by a seemingly ordinary tree that begins talking about it's day with {character.character_name}... weird\n+{xp_gained}xp", inline=False)

            if exploration_number == 21:
                embed.add_field(
                    name="-", value=f"During {character.character_name}'s travels they encounter a group of undercover demons", inline=False)
                capture_odds = random.randint(3, 7)
                if capture_odds >= character.character_level:
                    hp_lost = hp_suppresion(15, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} was captured, after being set free {character.character_name}'s head feels fuzzy\n-{hp_lost}hp", inline=False)
                else:
                    fight_odds = random.randint(7, 10)
                    if fight_odds <= character.character_level:
                        xp_gained = xp_suppresion(50, member)
                        hp_lost = hp_suppresion(random.randint(5, 15), member)
                        embed.add_field(
                            name="-", value=f"{character.character_name} beat up the demons and found that they plan on taking over the nearby area, interesting\n-{hp_lost}hp +{xp_gained}xp", inline=False)
                    else:
                        embed.add_field(
                            name="-", value=f"{character.character_name} fled and after being chased for awhile, {character.character_name} came upon a town and realized the demons disappeared.", inline=False)

            if exploration_number == 22:
                embed.add_field(
                    name="-", value=f"{character.character_name} found a castle in the middle of nowhere, {character.character_name} travelled here after learning about it's invinciblity in a nearby inn.", inline=False)
                if not character.character_level >= 30:
                    hp_lost = hp_suppresion(5, member)
                    embed.add_field(
                        name="-", value=f"{character.character_name} tries to punch the wall, ouch\n-{hp_lost}%hp", inline=False)
                else:
                    embed.add_field(
                        name="-", value=f"The wall shatters, huh...", inline=False)

            if exploration_number == 23:
                hp_lost = hp_suppresion(5, member)
                energy_stones_gained = 10
                embed.add_field(
                    name="-", value=f"A person appears infront of {character.character_name}, slaps {character.character_name} and disappears... they wonder why that happened until they find that they feel sick.\n-{hp_lost}%hp +{energy_stones_gained} Energy Stones", inline=False)

            if exploration_number == 24:
                xp_gained = xp_suppresion(15, member)
                embed.add_field(
                    name="-", value=f"{character.character_name} finds a group of people, dancing on a hill. They join in on the fun, how exhilerating!\n+{xp_gained}xp", inline=False)

            if exploration_number == 25:
                embed.add_field(
                    name="-", value=f"During {character.character_name}'s travels they encounter a person that starts saying that they're possessed", inline=False)

                fight_odds = random.randint(3, 7)
                if character.character_level >= fight_odds:
                    xp_gained = xp_suppresion(35, member)
                    hp_lost = hp_suppresion(10, member)
                    embed.add_field(
                        name="-", value=f"The person attacks you, you successfully defended yourself.\n+{xp_gained}xp -{hp_lost}%hp", inline=False)

                else:
                    hp_lost = hp_suppresion(10, member)
                    embed.add_field(
                        name="-", value=f"The person attacks you, you were beaten up.\n-{hp_lost}%hp", inline=False)

        elif character.character_world_level == 2:
            if exploration_number == 1:
                pass

        character_update(hp_lost, xp_gained, energy_stones_gained, member)

        dead = death_check(hp_lost, member)
        if dead:
            embed.add_field(name=f"Character Death",
                            value=f"{character.character_name} died, but they don't know that they've died.", inline=False)

        await self.send_message(interaction, embed)

    @app_commands.command()
    async def stats(self, interaction: discord.Interaction):
        member = interaction.user
        character = Character(member)
        if character.character_name == None:
            embed = discord.Embed(
                description="You don't have a character yet, do '$register (character name)' to create a character!", colour=0x800080)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if character.stat_birthday == 1651019868:
            stat_birthday = "The Primordial Era"
        else:
            stat_birthday = f"<t:{character.stat_birthday}:d>"
        stat_xp_gained = number_format(character.stat_xp_gained)
        stat_explorations = number_format(character.stat_explorations)
        stat_damage_taken = number_format(character.stat_damage_taken)
        stat_energy_stones_gained = number_format(
            character.stat_energy_stones_gained)

        embed = default_embed("Character Statistics", member=member)
        embed.add_field(name="Total Explorations:",
                        value=f"{stat_explorations}", inline=False)
        embed.add_field(name="Total Damage Taken:",
                        value=f"{stat_damage_taken}", inline=False)
        embed.add_field(name="Total Experience Gained",
                        value=f"{stat_xp_gained}", inline=False)
        embed.add_field(name="Total Energy Stones Gained",
                        value=f"{stat_energy_stones_gained}", inline=False)
        embed.add_field(name="Character's Birthday",
                        value=f"{stat_birthday}", inline=False)
        await self.send_message(interaction, embed)

    @app_commands.command()
    async def rankings(self, interaction: discord.Interaction):
        member = interaction.user
        character = Character(member)
        if character.character_name == None:
            embed = default_embed(
                "You don't have a character yet, do '$register (character name)' to create a character!", member=member)
            await self.send_message(interaction, embed)
            return
        with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
            cursor = db.cursor()
            cursor.execute(
                f"SELECT character_name, character_level, character_xp FROM incremental GROUP BY character_name ORDER BY 2 DESC, 3 DESC LIMIT 10")
            lb = cursor.fetchall()
            cursor.execute(
                f"SELECT character_name, character_level, character_xp FROM incremental WHERE member_id = ?", (member.id,))
            rank = cursor.fetchone()
        embed = default_embed(title="Advancement Rankings", description=f":first_place: **{lb[0][0]}** Level: {lb[0][1]} XP: {lb[0][2]}\n:second_place: **{lb[1][0]}** Level: {lb[1][1]} XP: {lb[1][2]}\n:third_place: **{lb[2][0]}** Level: {lb[2][1]} XP: {lb[2][2]}\n:medal: **{lb[3][0]}** Level: {lb[3][1]} XP: {lb[3][2]}\n:medal: **{lb[4][0]}** Level: {lb[4][1]} XP: {lb[4][2]}\n:medal: **{lb[5][0]}** Level: {lb[5][1]} XP: {lb[5][2]}\n:medal: **{lb[6][0]}** Level: {lb[6][1]} XP: {lb[6][2]}\n:medal: **{lb[7][0]}** Level: {lb[7][1]} XP: {lb[7][2]}\n:medal: **{lb[8][0]}** Level: {lb[8][1]} XP: {lb[8][2]}\n:medal: **{lb[9][0]}** Level: {lb[9][1]} XP: {lb[9][2]}\n\nYour character:\n**{rank[0]}** Level: {rank[1]} XP: {rank[2]}", member=member)
        await self.send_message(interaction, embed)


async def setup(bot: commands.Bot):
    print("Incremental Cog Ready")
    await bot.add_cog(Incremental(bot), guilds=[discord.Object(id=725164114506285066)])
