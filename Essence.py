# Discord API --------------------------------------------------
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

# from SensitiveData import Server

# Privileged intents --------------------------------------------------
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

# Help Command --------------------------------------------------


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)


# Bot Config --------------------------------------------------
bot = commands.Bot(command_prefix="$", intents=intents)
guild = 725164114506285066


@bot.command(name="sync")  # Sync Command
@commands.is_owner()
async def sync(ctx: commands.Context):
    try:
        async with ctx.typing():
            await bot.tree.sync(guild=discord.Object(id=725164114506285066))
    except Exception as e:
        await ctx.send(f"An error occured\n`{e}`", delete_after=5)
    else:
        await ctx.send("Done!", delete_after=5)

# Cogs --------------------------------------------------


async def loadExtensions():
    await bot.load_extension('Cogs.commands')  # Misc commands
    await bot.load_extension('Cogs.user')  # $profile related commands
    await bot.load_extension('Cogs.parties')  # $party related commands
    await bot.load_extension('Cogs.incremental')  # Incremental game commands
    await bot.load_extension('Cogs.staff')  # Staff commands
    await bot.load_extension('Cogs.errors')  # Error Handler
    await bot.load_extension('Cogs.items')  # $item related commands
# Server --------------------------------------------------
# Server.Server() WIP Server caller

# Bot Events -------------------------------------------


@bot.event  # Bot status
async def on_ready():
    await loadExtensions()
    with sqlite3.connect('Python/essence-bot/sensitive-data/essence.db') as db:
        cursor = db.cursor()
    cursor.execute(f"SELECT status FROM server WHERE party = ?", ('spirit',))
    result = cursor.fetchone()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(result[0]))
    print("Playing with Essence")

# Token --------------------------------------------------

load_dotenv()
Token = getenv("TOKEN")
bot.run(Token)
